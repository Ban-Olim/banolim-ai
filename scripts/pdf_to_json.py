import os
import glob
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from pdf.service import extract_book

# PDF → JSON 변환 스크립트
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR  = os.path.join(BASE_DIR, "scripts", "data", "raw")
JSON_DIR = os.path.join(BASE_DIR, "scripts", "data", "json")

def main():
    os.makedirs(JSON_DIR, exist_ok=True)

    pdf_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.pdf")))
    if not pdf_files:
        print(f"PDF 파일 없음: {RAW_DIR}")
        return

    print(f"{len(pdf_files)}개 PDF 처리 시작...\n")

    for pdf_path in pdf_files:
        book_id = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"[{book_id}] 처리 중...")
        try:
            data = extract_book(pdf_path)
            out_path = os.path.join(JSON_DIR, f"{data.book_id}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data.model_dump(), f, ensure_ascii=False, indent=2)
            print(f"  → 완료: {data.total_sentences}문장 저장 ({out_path})\n")
        except Exception as e:
            print(f"  → 오류: {e}\n")

if __name__ == "__main__":
    main()
