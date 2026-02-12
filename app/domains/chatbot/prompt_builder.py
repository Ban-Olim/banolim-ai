# 챗봇 system prompt 조립
# character_id(1~4), user_name, user_age, current_temperature로 character_N.txt 읽고 치환

from pathlib import Path

# 프롬프트 디렉터리: prompt_builder.py → chatbot → domains → app
_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "chatbot"
VALID_CHARACTER_IDS = (1, 2, 3, 4)

def build_system_prompt(
    character_id: int,
    user_name: str,
    user_age: int,
    current_temperature: int = 0,
) -> str:
    
    if character_id not in VALID_CHARACTER_IDS:
        raise ValueError(f"character_id는 1~4 중 하나여야 합니다. 받은 값: {character_id}")

    path = _PROMPTS_DIR / f"character_{character_id}.txt"
    if not path.exists():
        raise ValueError(f"캐릭터 프롬프트 파일이 없습니다: {path}")

    raw = path.read_text(encoding="utf-8")

    age_str = str(user_age)
    temp_str = str(max(0, min(100, current_temperature)))

    return raw.replace("{user_name}", user_name).replace("{user_age}", age_str).replace("{current_temperature}", temp_str)
