import os
import re

import fitz

from .client import page_to_base64, extract_sentences_from_page
from schemas import BookData

# 파일명 → (레벨, 제목)
def _parse_filename(filename: str) -> tuple[int, str]:
    stem = os.path.splitext(filename)[0]
    match = re.match(r"Lv(\d+)_(.+)", stem)
    if match:
        return int(match.group(1)), match.group(2)
    return 0, stem

# PDF → 책 데이터(BookData)
def extract_book(pdf_path: str) -> BookData:
    filename = os.path.basename(pdf_path)
    level, title = _parse_filename(filename)
    book_id = os.path.splitext(filename)[0]

    doc = fitz.open(pdf_path)
    all_sentences = []
    
    for page_num, page in enumerate(doc):
        print(f"    페이지 {page_num + 1}/{len(doc)} 처리 중...", end=" ")
        b64 = page_to_base64(page)
        sentences = extract_sentences_from_page(b64, page_num)
        print(f"{len(sentences)}문장")
        all_sentences.extend(sentences)
    
    # 페이지마다 추출한 문장들을 모두 합쳐서 책 데이터로 반환
    return BookData(
        book_id=book_id,
        level=level,
        title=title,
        total_sentences=len(all_sentences),
        sentences=all_sentences,
    )
