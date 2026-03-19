from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "sentence"

def build_quiz_prompt(
    user_age: int,
    count: int,
    rag_examples: str,
) -> str:
    path = _PROMPTS_DIR / "quiz.md"
    if not path.exists():
        raise ValueError(f"퀴즈 프롬프트 파일이 없습니다: {path}")

    raw = path.read_text(encoding="utf-8")
    return (
        raw
        .replace("{user_age}", str(user_age))
        .replace("{count}", str(count))
        .replace("{rag_examples}", rag_examples)
    )
