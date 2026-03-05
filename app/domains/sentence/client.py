# 문장 분해 OPENAI_API_KEY를 사용함. 
# 문장 분해 API를 호출하고, 응답에서 sentences 리스트를 반환하도록 함.
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 프로젝트 루트의 .env 로드 (client.py → chatbot → domains → app → banolim-ai 이므로 4단계 상위)
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

# OpenAI 클라이언트 생성 함수
def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return OpenAI(api_key=api_key)

