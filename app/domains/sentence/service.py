## 요청 처리 → DB 조회 → 프롬프트 조립 → Claude 호출(Caching) → TTS -> 응답 변환
from pydantic_core import ValidationError
from fastapi import HTTPException

from . import client, prompt_builder, db_client, tts_client
from .schemas import SentenceRequest, SentenceResponse, SentenceProblemModel

# RAG 예시로 사용할 문장 수 (생성할 문제 수의 몇 배를 가져올지)
_RAG_SAMPLE_MULTIPLIER = 2

def _age_to_level(user_age: int) -> int:
    if user_age <= 8:
        return 2
    elif user_age <= 10:
        return 3
    elif user_age == 11:
        return 4
    else:
        return 5

def _format_rag_examples(sentences: list[str]) -> str:
    return "\n".join(f"{i + 1}. {s}" for i, s in enumerate(sentences))

# 커스텀 예외 메세지 생성
def _get_error_response(message:str) -> SentenceResponse:
    error_object = SentenceProblemModel(
        sentence=message,
        slots=[],
        options=[],
        targetAge=0,
        sentence_audio_base64=""
    )
    return SentenceResponse(problems=[error_object])

# 문장 생성 
def create_generate_sentence(req: SentenceRequest) -> SentenceResponse:
    # 1. DB 조회 단계 
    try:
        level = _age_to_level(req.user_age)
        fetch_count = min(req.count * _RAG_SAMPLE_MULTIPLIER, 30)
        sentences = db_client.get_sentences_by_level(level, fetch_count)
        print(sentences)

        if not sentences:
            return _get_error_response("나이에 맞는 문장 데이터를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return _get_error_response("데이터베이스에서 문장을 가져오는 데 실패했습니다.")

    # 2. 프롬프트 조립
    try:
        rag_examples = _format_rag_examples(sentences)

        system_rules, user_data = prompt_builder.build_quiz_prompt(
            user_age=req.user_age,
            count=req.count,
            rag_examples=rag_examples
        )
    except Exception as e:
        print(f"[PROMPT ERROR] {e}")
        return _get_error_response("문제 생성 프롬프트를 만드는 중 오류가 발생했습니다.")

    # 3. Claude 호출
    try:
        raw_problems = client.generate_sentence(
            system_prompt=system_rules,
            user_input=user_data
        )
        if not raw_problems:
            raise ValueError("AI가 문제를 생성하지 않았습니다.")

    except Exception as e:
        print(f"[AI ERROR] {e}")
        return _get_error_response("현재 접속자가 너무 많아 AI가 답변을 고민하고 있어요! 잠시 후 다시 시도해주세요.")
    except Exception as e:
        print(f"[AI ERROR] {e}")
        return _get_error_response("AI 서버와 연결이 원활하지 않습니다.")

    # 4. 검증 및 TTS 생성
    validated_problems = []
    try:
        for idx, problem_dict in enumerate(raw_problems):
            try:
                validated_model = SentenceProblemModel(**problem_dict)
            
                # TTS 오디오 생성 및 base64 인코딩
                audio_base64 = tts_client.generate_sentence_audio_base64(
                    text=validated_model.sentence,
                    user_age=req.user_age
                )
                validated_model.sentence_audio_base64 = audio_base64
                validated_problems.append(validated_model)
        
            except ValidationError as ve:
                    print(f"[VALIDATION ERROR] {idx+1}번째 문제 형식이 맞지 않음: {ve}")
                    continue
            except Exception as te:
                print(f"[TTS ERROR] {idx+1}번째 문제 음성 생성 실패: {te}")
                continue

        if not validated_problems:
            return _get_error_response("유효한 문제를 생성하지 못했습니다. 다시 시도해 볼까요?")
    
    except Exception as e:
        print(f"[FINAL PROCESS ERROR] {e}")
        return _get_error_response("문장 처리 과정에서 예기치 못한 오류가 발생했습니다.")
    
    return SentenceResponse(problems=validated_problems)