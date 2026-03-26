# 문장 분해 API 요청/응답 스키마 (Spring Boot ↔ FastAPI)
from pydantic import BaseModel, Field
from typing import List, Optional

# Spring Boot -> FastAPI 요청 body
class SentenceRequest(BaseModel):
    user_age: int 
    count: int 

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
    targetAge: int 
    sentence_audio_base64: Optional[str] = None

# 3. 최종 API 응답 스키마 (문제들의 배열을 감싸는 래퍼)
class SentenceResponse(BaseModel):
    problems: List[SentenceProblemModel]