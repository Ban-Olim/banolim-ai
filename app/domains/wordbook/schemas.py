from pydantic import BaseModel, Field
from typing import List, Optional

# OpenAI API 요청 Body
class WordbookRequest(BaseModel):
    lemma: str = Field(..., description="단어 (기본형)")
    definition: str = Field(..., description="단어의 의미")
    pos: str = Field(..., description="품사")

# OpenAI API 응답 Body
class WordbookResponse(BaseModel):
    example_sentence: str = Field(..., description="초등학생 눈높이에 맞춘 예문")
    translation: str = Field(..., description="예문의 한국어 번역 (또는 설명)")
