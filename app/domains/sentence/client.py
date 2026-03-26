 # 문장 분해 Claude API를 호출하고, 응답에서 sentences 리스트를 반환하도록 함.
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import anthropic

from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

# Claude 클라이언트 생성 함수
def _get_client() -> anthropic.Anthropic:
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise ValueError("CLAUDE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return anthropic.Anthropic(api_key=api_key)

def generate_sentence(
        system_prompt: str,
        user_input: str,
        model: str = "claude-sonnet-4-6",
        temperature: float = 0.7,
) -> List[Dict[str, Any]]:
    
    # Claude 클라이언트 + 메시지 생성
    client = _get_client()
    content=""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            temperature=temperature,
            system=system_prompt, 
            messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        }
    ],
)
        # 응답에서 content 추출
        content = response.content[0].text.strip()

        # JSON 추출 및 [] sentences 반환
        if content.startswith("```json"):
            content = content.replace("```json", "", 1).rsplit("```", 1)[0].strip()
        elif content.startswith("```"):
            content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()

        # {"problems": [...]} 형태로 파싱
        result_data = json.loads(content)
        return result_data.get("problems", [])
    
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"JSON 파싱 오류: {e}")
        print(f"원본 응답: {content}")
        return []
    except Exception as e:
        print(f"Claude API 통신 에러: {e}")
        return []