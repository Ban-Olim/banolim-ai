# 문장 분해 system prompt 조립
# user_age, difficulty, count, topic_words로 quiz.md 템플릿 읽고 치환

from pathlib import Path
from typing import List

# 프롬프트 디렉터리: prompt_builder.py → sentence → domains → app
_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "sentence"

DIFFICULTY_EXAMPLES = {
    1: '''{
        "sentence": "예쁜 고양이가 생선을 먹는다.",
        "difficulty": 1,
        "slots": [
            { "slotOrder": 1, "slotLabel": "어떤", "correctAnswer": "예쁜" },
            { "slotOrder": 2, "slotLabel": "누가", "correctAnswer": "고양이가" },
            { "slotOrder": 3, "slotLabel": "무엇을", "correctAnswer": "생선을" },
            { "slotOrder": 4, "slotLabel": "했나요", "correctAnswer": "먹는다" }
        ],
        "options": ["예쁜", "고양이가", "생선을", "먹는다"]
    }''',
    2: '''{
        "sentence": "어제 우리 동생이 뛰었다.",
        "difficulty": 2,
        "slots": [
            { "slotOrder": 1, "slotLabel": "언제", "correctAnswer": "어제" },
            { "slotOrder": 2, "slotLabel": "누가", "correctAnswer": "우리 동생이" },
            { "slotOrder": 3, "slotLabel": "", "correctAnswer": "" },
            { "slotOrder": 4, "slotLabel": "했나요", "correctAnswer": "뛰었다" }
        ],
        "options": ["어제", "우리 동생이", "뛰었다"]
    }''',
    3: '''{
        "sentence": "쉬는 시간에 내 짝꿍이 그림책을 읽는다.",
        "difficulty": 3,
        "slots": [
            { "slotOrder": 1, "slotLabel": "언제", "correctAnswer": "쉬는 시간에" },
            { "slotOrder": 2, "slotLabel": "누가", "correctAnswer": "내 짝꿍이" },
            { "slotOrder": 3, "slotLabel": "무엇을", "correctAnswer": "그림책을" },
            { "slotOrder": 4, "slotLabel": "했나요", "correctAnswer": "읽는다" }
        ],
        "options": ["쉬는 시간에", "내 짝꿍이", "그림책을", "읽는다"]
    }''',
    4: '''{
        "sentence": "비가 많이 와서 우리는 교실에서 논다.",
        "difficulty": 4,
        "slots": [
            { "slotOrder": 1, "slotLabel": "왜 그랬나요?", "correctAnswer": "비가 많이 와서" },
            { "slotOrder": 2, "slotLabel": "누가", "correctAnswer": "우리는" },
            { "slotOrder": 3, "slotLabel": "어디서", "correctAnswer": "교실에서" },
            { "slotOrder": 4, "slotLabel": "했나요", "correctAnswer": "논다" }
        ],
        "options": ["비가 많이 와서", "우리는", "교실에서", "논다"]
    }''',
    5: '''{
            "sentence": "손을 깨끗이 씻고 나는 사과를 맛있게 먹었다.",
            "difficulty": 5,
            "targetAge": 9,
            "slots": [
                { "slotOrder": 1, "slotLabel": "먼저 무슨 일을 했나요?", "correctAnswer": "손을 깨끗이 씻고", "hint": "처음 한 행동" },
                { "slotOrder": 2, "slotLabel": "누가", "correctAnswer": "나는", "hint": "주인공" },
                { "slotOrder": 3, "slotLabel": "무엇을", "correctAnswer": "사과를", "hint": "먹은 것" },
                { "slotOrder": 4, "slotLabel": "그 다음 어떻게 했나요?", "correctAnswer": "맛있게 먹었다", "hint": "나중 행동" }
            ],
            "options": ["손을 깨끗이 씻고", "나는", "사과를", "맛있게 먹었다"]
        }'''
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
