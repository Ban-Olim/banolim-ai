# 문장 분해 OPENAI_API_KEY를 사용함. 
# 문장 분해 API를 호출하고, 응답에서 sentences 리스트를 반환하도록 함.
import json
import os
from pathlib import Path
from typing import List, Dict, Any

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

def generate_sentence(
        system_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
) -> List[Dict[str, Any]]:
    
    # OpenAI 클라이언트 + 메시지 생성
    client = _get_client()
    api_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "위 규칙에 맞게 문장 분해 문제 생성을 시작해줘."}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        # 응답에서 content 추출
        content = response.choices[0].message.content or "" 

        # JSON 추출 및 [] sentences 반환
        content = content.strip()
        if content.startswith("```json"):
            content = content.strip("```json").strip("```").strip()
        elif content.startswith("```"):
            content = content.strip("```").strip()

        # {"problems": [...]} 형태로 파싱
        result_data = json.loads(content)
        return result_data.get("problems", [])
    
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"JSON 파싱 오류: {e}")
        print(f"원본 응답: {content}")
        return []
    except Exception as e:
        print(f"OpenAI API 통신 에러: {e}")
        return []