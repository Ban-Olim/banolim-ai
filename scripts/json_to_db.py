import os
import glob
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from db.connection import get_conn
from db.schema import init_db
from db.repository import upsert_book, upsert_sentences
from schemas import BookData

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, "scripts", "data", "json")

def main():
    json_files = sorted(glob.glob(os.path.join(JSON_DIR, "*.json")))
    if not json_files:
        print(f"JSON 파일 없음: {JSON_DIR}")
        return

    conn = get_conn()
    print("PostgreSQL 연결 성공\n")

    init_db(conn)
    print()

    total = 0
    for json_path in json_files:
        with open(json_path, encoding="utf-8") as f:
            data = BookData(**json.load(f))
        print(f"[{data.book_id}] 처리 중...")
        upsert_book(conn, data.book_id, data.level)
        upsert_sentences(conn, data.book_id, data.level, data.sentences)
        print(f"  → {len(data.sentences)}문장 삽입 완료\n")
        total += len(data.sentences)

    conn.close()
    print(f"전체 완료: {total}문장 → sentences 테이블")

if __name__ == "__main__":
    main()
