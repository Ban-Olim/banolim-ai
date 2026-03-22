## 요청 처리 → DB 조회 → 프롬프트 조립 → OpenAI 호출 → TTS -> 응답 변환
from pydantic_core import ValidationError
from fastapi import HTTPException

from . import client, prompt_builder, db_client, tts_client
from .schemas import SentenceRequest, SentenceResponse, SentenceProblemModel

# RAG 예시로 사용할 문장 수 (생성할 문제 수의 몇 배를 가져올지)
_RAG_SAMPLE_MULTIPLIER = 2

# 나이를 레벨로 변환 (7-8세→2, 9-10세→3, 11세→4, 12-13세→5)
def _age_to_level(user_age: int) -> int:
    if user_age <= 8:
        return 2
    elif user_age <= 10:
        return 3
    elif user_age == 11:
        return 4
    else:
        return 5

# RAG 예시들을 번호 매겨서 문자열로 포맷팅
def _format_rag_examples(sentences: list[str]) -> str:
    return "\n".join(f"{i + 1}. {s}" for i, s in enumerate(sentences))

# 문장 생성 
def create_generate_sentence(req: SentenceRequest) -> SentenceResponse:

    # DB에서 나이 수준에 맞는 문장 조회
    level = _age_to_level(req.user_age)
    fetch_count = min(req.count * _RAG_SAMPLE_MULTIPLIER, 30)
    try:
        sentences = db_client.get_sentences_by_level(level, fetch_count)
    except Exception as e:
        print(f"DB 조회 오류: {e}")
        raise ValueError("문장 데이터를 가져오는 중 오류가 발생했습니다.")

    if not sentences:
        raise HTTPException(status_code=500, detail="해당 나이 수준의 문장 데이터가 없습니다.")

    # 프롬프트 조립
    try:
        rag_examples = _format_rag_examples(sentences)
        system_prompt = prompt_builder.build_quiz_prompt(
            user_age=req.user_age,
            count=req.count,
            rag_examples=rag_examples,
        )
    except Exception as e:
        print(f"프롬프트 조립 오류: {e}")
        raise ValueError("프롬프트를 준비하는 중 오류가 발생했습니다.")

    # OpenAI 호출
    raw_problems = client.generate_sentence(system_prompt=system_prompt)
    if not raw_problems:
        raise HTTPException(
            status_code=500,
            detail="AI가 문제 생성에 실패했거나 올바른 JSON을 반환하지 않았습니다."
        )

    # validation & 변환: raw_problems (List[Dict]) → List[SentenceProblemModel]
    validated_problems = []
    for idx, problem_dict in enumerate(raw_problems):
        try:
            validated_model = SentenceProblemModel(**problem_dict)
            
            audio_base64 = tts_client.generate_sentence_audio_base64(
                text=validated_model.sentence,
                user_age=req.user_age
            )
            validated_model.sentence_audio_base64 = audio_base64
            validated_problems.append(validated_model)
        
        except ValidationError as e:
            print(f"[경고] {idx+1}번째 문제 파싱 실패. 해당 문제를 건너뜁니다: {e}")
            continue

    if not validated_problems:
        raise HTTPException(
            status_code=500,
            detail="AI가 반환한 문제들 중 유효한 형식의 문제가 하나도 없습니다."
        )
    return SentenceResponse(problems=validated_problems)