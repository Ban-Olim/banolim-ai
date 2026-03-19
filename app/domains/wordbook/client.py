import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 프로젝트 루트의 .env 로드
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

# OpenAI 클라이언트 생성 함수
def _get_client() -> OpenAI:
    api_key = os.getenv("WORDBOOK_OPENAI_API_KEY") or os.getenv("CHATBOT_OPENAI_API_KEY")
    if not api_key:
        raise ValueError("WORDBOOK_OPENAI_API_KEY 또는 CHATBOT_OPENAI_API_KEY가 설정되지 않았습니다.")
    return OpenAI(api_key=api_key)

def generate(
    system_prompt: str,
    messages: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> dict:
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

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 원문 반환 (혹은 에러 처리)
        return {"example_sentence": content, "translation": ""}
