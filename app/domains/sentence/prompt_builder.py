# 문장 분해 system prompt 조립
# user_age, difficulty, count, topic_words로 quiz.md 템플릿 읽고 치환

from pathlib import Path
from typing import List

# 프롬프트 디렉터리: prompt_builder.py → sentence → domains → app
_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "sentence"

DIFFICULTY_EXAMPLES = {
    1: 
    '''{
        "sentence": "예쁜 고양이가 생선을 먹는다.",
        "hintLabels": ["어떤/언제", "누가", "무엇을", "했나요"],
        "decomposition": { "slot1": "예쁜", "slot2": "고양이가", "slot3": "생선을", "slot4": "먹는다" },
        "difficulty": 1
    }''',
    2: 
    '''{
        "sentence": "어제 우리 동생이 우유를 마셨다.",
        "hintLabels": ["어떤/언제", "누가", "무엇을", "했나요"],
        "decomposition": { "slot1": "어제", "slot2": "우리 동생이", "slot3": "우유를", "slot4": "마셨다" },
        "difficulty": 2
    }''',
    3: 
    '''{
        "sentence": "쉬는 시간에 내 짝꿍이 그림책을 읽는다.",
        "hintLabels": ["어떤/언제", "누가", "무엇을", "했나요"],
        "decomposition": { "slot1": "쉬는 시간에", "slot2": "내 짝꿍이", "slot3": "그림책을", "slot4": "읽는다" },
        "difficulty": 3
    }''',
    4: 
    '''{
        "sentence": "비가 많이 와서 우리는 교실에서 논다.",
        "hintLabels": ["왜 그랬나요?", "누가", "어디서/무엇을", "했나요"],
        "decomposition": { "slot1": "비가 많이 와서", "slot2": "우리는", "slot3": "교실에서", "slot4": "논다" },
        "difficulty": 4
    }''',
    5: 
    '''{
        "sentence": "방 청소를 끝내고 나는 엄마와 퍼즐을 맞췄다.",
        "hintLabels": ["먼저 무슨 일을 했나요?", "누가", "무엇을", "그 다음 어떻게 했나요?"],
        "decomposition": { "slot1": "방 청소를 끝내고", "slot2": "나는", "slot3": "엄마와 퍼즐을", "slot4": "맞췄다" },
        "difficulty": 5
    }''',
}

def build_quiz_prompt(
    user_age: int,
    difficulty: int,
    count: int,
    topic_words: List[str],
) -> str:

    path = _PROMPTS_DIR / "quiz.md"
    if not path.exists():
        raise ValueError(f"퀴즈 프롬프트 파일이 없습니다: {path}")
    
    if difficulty not in DIFFICULTY_EXAMPLES:
        raise ValueError(f"지원하지 않는 난이도입니다: {difficulty}")

    raw = path.read_text(encoding="utf-8")

    return (
        raw
        .replace("{user_age}", str(user_age))
        .replace("{difficulty}", str(difficulty))
        .replace("{count}", str(count))
        .replace("{topic_words}", ", ".join(topic_words))
        .replace("{difficulty_example}", DIFFICULTY_EXAMPLES[difficulty])  # 추가
    )
