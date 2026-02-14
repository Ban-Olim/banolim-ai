
# 챗봇 전용 OpenAI 클라이언트
#CHATBOT_OPENAI_API_KEY를 사용해 채팅 완성 API를 호출하고, 응답에서 message/temperature를 반환하도록 함

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
    api_key = os.getenv("CHATBOT_OPENAI_API_KEY")
    if not api_key:
        raise ValueError("CHATBOT_OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return OpenAI(api_key=api_key)

# 채팅 완성 API 호출 함수
def generate(
    system_prompt: str,
    messages: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> dict:
    
    # OpenAI 클라이언트 + 메시지 생성
    client = _get_client()
    api_messages = [{"role": "system", "content": system_prompt}]
    api_messages.extend(messages)

    response = client.chat.completions.create(
        model=model,
        messages=api_messages,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or ""

    # JSON 추출
    message_text = content.strip()
    temperature_value = 0
    try:
        obj = json.loads(content)
        message_text = obj.get("message", message_text)
        temperature_value = int(obj.get("temperature", 0))
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    # temperature 0~100 범위로 보정
    temperature_value = max(0, min(100, temperature_value))

    return {"message": message_text, "temperature": temperature_value}
