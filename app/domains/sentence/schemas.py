# 문장 분해 API 요청/응답 스키마 (Spring Boot ↔ FastAPI)
from pydantic import BaseModel, Field
from typing import List

# Spring Boot -> FastAPI 요청 body
class SentenceRequest(BaseModel):
    user_age: int = Field(..., ge=7, le=13, description="입력받은 사용자 나이")
    difficulty: int = Field(..., ge=1, le=5, description="난이도 (1~5단계). 문장의 길이와 구조, 힌트 라벨을 결정.")
    count: int = Field(..., ge=1, description="한 번에 생성할 문제 개수 (일반적으로 한 챕터당 10개)")

# 1. 개별 슬롯 스키마
class SlotModel(BaseModel):
    slotOrder: int  
    slotLabel: str 
    correctAnswer: str 
    hint: str = "" # 보조 힌트

# 2. 개별 문제 스키마 
class SentenceProblemModel(BaseModel):
    sentence: str
    slots: List[SlotModel]  
    options: List[str] 
    difficulty: int 
    targetAge: int 

# 3. 최종 API 응답 스키마 (문제들의 배열을 감싸는 래퍼)
class SentenceResponse(BaseModel):
    problems: List[SentenceProblemModel] = Field(
        ..., 
        description="생성된 문장 분해 문제 리스트"
    )