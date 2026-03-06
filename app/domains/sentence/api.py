# 문장분해 HTTP 진입점 (Spring Boot Controller 역할)

from fastapi import APIRouter
from .schemas import SentenceResponse, SentenceRequest
from . import service

router = APIRouter(prefix="/sentence", tags=["sentence"])

# 문장 분해 문제 생성 API
@router.post("/generate", response_model=SentenceResponse)
def generate(body: SentenceRequest) -> SentenceResponse:
    return service.create_generate_sentence(body)