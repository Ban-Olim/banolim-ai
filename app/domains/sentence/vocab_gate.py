# vocab_gate.json파일을 로드하여 문제 생성에 필요한 함수를 정의함. 

import json
import random
from pathlib import Path
from typing import List


_VOCAB_GATE_PATH = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "sentence" / "vocab_gate.json"
_SAMPLE_SIZE = 20   # 프롬프트에 주입할 단어 수

# JSON 파일에서 단어 목록 로드
def _load_vocab_gate() -> dict:
    if not _VOCAB_GATE_PATH.exists():
        raise FileNotFoundError(f"vocab_gate.json 파일이 없습니다: {_VOCAB_GATE_PATH}")
    with _VOCAB_GATE_PATH.open(encoding="utf-8") as f:
        return json.load(f)
    
_gate = _load_vocab_gate()
_allowed_set: set[str] = set(_gate["allowed_words"]) # 검증용 허용 단어 집합
_grade_topics: dict[str, list[str]] = _gate["grade_topics"] # 나이별 단어 풀

# user_age에 맞는 단어 20개 추출
def get_topic_words(user_age: int) -> List[str]:
    age_key = str(user_age)
    if age_key not in _grade_topics:
        raise ValueError(f"지원되지 않는 나이입니다: {user_age} 허용 범위: 7~13)")
    
    pool = _grade_topics[age_key]
    sample_size = min(_SAMPLE_SIZE, len(pool))
    return random.sample(pool, sample_size)
