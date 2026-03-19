import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

# DB에서 특정 레벨의 문장을 랜덤하게 조회하는 함수
_FETCH_SENTENCES = """
SELECT text FROM sentences WHERE level = %s ORDER BY RANDOM() LIMIT %s;
"""

# DB 연결 및 문장 조회 함수
def get_sentences_by_level(level: int, count: int) -> list[str]:
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("PORT", 5432)),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    try:
        with conn.cursor() as cur:
            cur.execute(_FETCH_SENTENCES, (level, count))
            rows = cur.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()
