from pathlib import Path
from typing import List
from jinja2 import Template

# 프롬프트 파일 경로 설정
_PROMPT_DIR = Path(__file__).resolve().parents[2] / "llm" / "prompts" / "wordbook"

def _load_prompt(filename: str) -> str:
    with open(_PROMPT_DIR / filename, "r", encoding="utf-8") as f:
        return f.read()

def build_system_prompt() -> str:
    return _load_prompt("system_prompt.txt")

def build_user_prompt(lemma: str, definition: str, pos: str) -> str:
    template_str = _load_prompt("user_prompt.txt")
    template = Template(template_str)
    
    return template.render(lemma=lemma, definition=definition, pos=pos)
