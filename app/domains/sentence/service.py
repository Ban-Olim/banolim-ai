# 문장분해 비즈니스 로직
# req 요청 -> openAI 호출 -> validation -> 응답 반환
from operator import index

from pydantic_core import ValidationError
from fastapi import HTTPException

from . import client, prompt_builder
from .schemas import SentenceRequest, SentenceResponse, SentenceProblemModel, SentenceDecomposition
from typing import List, Dict, Any
import json     

def create_generate_sentence(req: SentenceRequest) -> SentenceResponse:
    
    # 프롬프트 조립
    try: 
        system_prompt = prompt_builder.build_quiz_prompt(
        user_age=req.user_age,
        difficulty=req.difficulty,
        count=req.count,
    )
    except Exception as e:
        print(f"프롬프트 조립 오류: {e}")
        raise ValueError("문제 생성에 필요한 프롬프트를 준비하는 중 오류가 발생했습니다.")
    
    # OpenAI 호출
    raw_problems = client.generate_sentence(
        system_prompt=system_prompt)
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
            validated_problems.append(validated_model)
        except ValidationError as e:
            print(f"[경고] {idx+1}번째 문제 파싱 실패. 해당 문제를 건너뜁니다: {e}")
            continue

    # 최소한 하나의 유효한 문제가 있어야 응답 반환
    if not validated_problems:
        raise HTTPException(
            status_code=500, 
            detail="AI가 반환한 문제들 중 유효한 형식의 문제가 하나도 없습니다."
        )
    return SentenceResponse(problems=validated_problems)
