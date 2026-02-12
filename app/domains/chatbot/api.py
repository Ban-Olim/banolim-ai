# 챗봇 HTTP 진입점 (Spring Boot Controller 역할)

from fastapi import APIRouter

from .schemas import ChatbotRequest, ChatbotResponse
from . import service

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# 챗봇 답변 생성 API
@router.post("/chat", response_model=ChatbotResponse)
def chat(body: ChatbotRequest) -> ChatbotResponse:
    return service.chat(body)
