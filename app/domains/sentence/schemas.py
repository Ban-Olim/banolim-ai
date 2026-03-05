# 문장 분해 API 요청/응답 스키마 (Spring Boot ↔ FastAPI)
from pydantic import BaseModel, Field
from typing import List

# Spring Boot -> FastAPI 요청 body
class SentenceGenerateRequest(BaseModel):
    user_age: int = Field(..., ge=7, le=13, description="입력받은 사용자 나이")
    difficulty: int = Field(..., ge=1, le=5, description="난이도 (1~5단계). 문장의 길이와 구조, 힌트 라벨을 결정.")
    count: int = Field(..., ge=1, description="한 번에 생성할 문제 개수 (일반적으로 한 챕터당 10개)")

# -----------------------------------
# FastAPI -> Spring Boot 응답 body
# -----------------------------------

# 1. 4구역 분해 조각 (Decomposition)
class SentenceDecomposition(BaseModel):
    slot1: str = Field(..., description="상황 또는 수식어 (예: 비가 많이 와서)")
    slot2: str = Field(..., description="주어 (예: 우리는)")
    slot3: str = Field(..., description="목적어 또는 부사어 (예: 교실에서)")
    slot4: str = Field(..., description="서술어 (예: 논다)")

# 2. 개별 문제 스키마 (AI가 생성하는 1개의 문제 단위)
class SentenceProblemModel(BaseModel):
    sentence: str = Field(
        ..., 
        description="생성된 전체 문장"
    )
    hintLabels: List[str] = Field(
        ..., 
        min_length=4, max_length=4, 
        description="프론트엔드에 표시될 4개의 힌트 라벨 배열"
    )
    decomposition: SentenceDecomposition = Field(
        ..., 
        description="4구역으로 분해된 문장 조각 객체"
    )
    difficulty: int = Field(
        ..., 
        description="해당 문장의 실제 난이도 (1-5)"
    )

# 3. 최종 API 응답 스키마 (문제들의 배열을 감싸는 래퍼)
class SentenceGenerateResponse(BaseModel):
    problems: List[SentenceProblemModel] = Field(
        ..., 
        description="생성된 문장 분해 문제 리스트"
    )