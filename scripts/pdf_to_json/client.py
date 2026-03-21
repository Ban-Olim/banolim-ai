import os
import re
import json
import base64

import fitz
from openai import OpenAI

from .prompt_builder import build_extraction_prompt

_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 페이지 → base64 인코딩된 이미지
def page_to_base64(page: fitz.Page, dpi: int = 150) -> str:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")

# 페이지 이미지 → 문장 리스트
def extract_sentences_from_page(b64_image: str, page_num: int) -> list[str]:
    response = _client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": build_extraction_prompt()},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}",
                            "detail": "high",
                        },
                    },
                    {"type": "text", "text": f"이 페이지({page_num + 1}p)의 문장을 추출해주세요."},
                ],
            },
        ],
        max_tokens=1000,
        temperature=0,
    )

    content = response.choices[0].message.content.strip()
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if not match:
        return []
    try:
        sentences = json.loads(match.group())
        return [
            s.strip()
            for s in sentences
            if isinstance(s, str) and len(s.strip().split()) >= 2
        ]
    except json.JSONDecodeError:
        return []
