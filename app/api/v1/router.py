# v1 API 라우터: 도메인별 라우터를 /v1 아래에 묶음

from fastapi import APIRouter

from app.domains.chatbot.api import router as chatbot_router

router = APIRouter()
router.include_router(chatbot_router)
