from pathlib import Path
from typing import Tuple

_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "sentence"

def build_quiz_prompt(
    user_age: int,
    count: int,
    rag_examples: str,
) -> Tuple[str, str]:  # (system_prompt, user_input) 튜플 반환
    
    path = _PROMPTS_DIR / "quiz.md"
    if not path.exists():
        raise ValueError(f"퀴즈 프롬프트 파일이 없습니다: {path}")

    raw_system_prompt = path.read_text(encoding="utf-8")

    user_input = (
        f"### 실시간 입력 데이터\n"
        f"- age: {user_age}\n"
        f"- count: {count}\n"
        f"- 대상 소재(RAG):\n{rag_examples}"
    )

    return raw_system_prompt, user_input
