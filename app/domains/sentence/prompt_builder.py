# 문장 분해 system prompt 조립
# suer_age, dificulty, count로 quiz.md 템플릿 읽고 치환

from pathlib import Path

# 프롬프트 디렉터리: prompt_builder.py → sentence → domains → app
_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "sentence"

def build_quiz_prompt(
    user_age: int,
    difficulty: int,
    count: int,
) -> str:

    path = _PROMPTS_DIR / "quiz.md"
    if not path.exists():
        raise ValueError(f"퀴즈 프롬프트 파일이 없습니다: {path}")

    raw = path.read_text(encoding="utf-8")

    age_str = str(user_age)
    difficulty_str = str(difficulty)
    count_str = str(count)

    return raw.replace("{user_age}", age_str).replace("{difficulty}", difficulty_str).replace("{count}", count_str)
