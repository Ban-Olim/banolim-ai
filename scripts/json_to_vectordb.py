import os
import glob
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from db.connection import get_conn
from db.schema import init_db
from embedding.service import embed_and_store
from schemas import BookData
# JSON → DB 임베딩 생성 및 저장 스크립트

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, "data", "json")

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
        book_id = os.path.splitext(os.path.basename(json_path))[0]
        print(f"[{book_id}] 처리 중...")
        with open(json_path, encoding="utf-8") as f:
            data = BookData(**json.load(f))
        count = embed_and_store(conn, data)
        print(f"  → {count}문장 삽입 완료\n")
        total += count

    conn.close()
    print(f"전체 완료: {total}문장 → sentences 테이블")

if __name__ == "__main__":
    main()
