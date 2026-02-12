# 챗봇 API 요청/응답 스키마 (Spring Boot ↔ FastAPI)

from typing import Literal, Optional

from pydantic import BaseModel, Field

# 사용자와 챗봇 답변 한 편
class ChatMessage(BaseModel):
    role: Literal["USER", "BOT"] = Field(..., description="발화자. USER(사용자) / BOT(챗봇)")
    content: str = Field(..., description="메시지 내용")

# Spring Boot → FastAPI 요청 body
class ChatbotRequest(BaseModel):
    character_id: int = Field(..., ge=1, le=4, description="캐릭터 번호 1~4")
    user_name: str = Field(..., description="대화 상대 이름")
    user_age: int = Field(..., description="대화 상대 나이")
    messages: list[ChatMessage] = Field(default_factory=list, description="대화 이력. 비어 있으면 첫 인사 생성")
    current_temperature: int = Field(0, ge=0, le=100, description="현재 마음 온도 0~100")

# FastAPI → Spring Boot 응답 body
class ChatbotResponse(BaseModel):
    message: str = Field(..., description="챗봇 답변")
    temperature: int = Field(..., ge=0, le=100, description="갱신된 마음 온도 0~100")
    audio_base64: Optional[str] = Field(None, description="TTS 음성 데이터 (Base64). 미구현 시 None. Spring Boot에서 S3 업로드 후 URL 생성")
