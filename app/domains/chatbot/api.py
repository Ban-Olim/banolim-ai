# 챗봇 HTTP 진입점 (Spring Boot Controller 역할)

from fastapi import APIRouter

from .schemas import ChatbotRequest, ChatbotResponse
from . import service

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/chat", response_model=ChatbotResponse)
def chat(body: ChatbotRequest) -> ChatbotResponse:
    """Spring Boot가 호출. 대화 이력 + 사용자 정보로 챗봇 답변 생성 후 반환."""
    return service.chat(body)
