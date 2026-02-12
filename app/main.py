# FastAPI 앱 진입점

from fastapi import FastAPI

from app.api.v1.router import router as v1_router

app = FastAPI(title="banolim-ai")
app.include_router(v1_router, prefix="/v1")
