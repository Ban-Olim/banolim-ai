import os

_PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "pdf_extraction.md")

# PDF에서 문장 추출하는 프롬프트 빌더
def build_extraction_prompt() -> str:
    with open(_PROMPT_PATH, encoding="utf-8") as f:
        return f.read()
