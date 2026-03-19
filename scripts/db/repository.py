
_INSERT_BOOK = """
INSERT INTO books (book_id, level)
VALUES (%s, %s)
ON CONFLICT (book_id) DO UPDATE SET
    level = EXCLUDED.level;
"""

_INSERT_SENTENCE = """
INSERT INTO sentences (book_id, level, idx, text, embedding)
VALUES (%s, %s, %s, %s, %s::vector)
ON CONFLICT (book_id, idx) DO UPDATE SET
    text      = EXCLUDED.text,
    embedding = EXCLUDED.embedding;
"""

# DB 관련 함수들 (테이블 생성, 데이터 삽입 등)
def upsert_book(conn, book_id: str, level: int):
    with conn.cursor() as cur:
        cur.execute(_INSERT_BOOK, (book_id, level))

def upsert_sentences(
    conn,
    book_id: str,
    level: int,
    sentences: list[str],
    embeddings: list[list[float]],
):
    rows = [
        (book_id, level, idx, text, str(emb))
        for idx, (text, emb) in enumerate(zip(sentences, embeddings))
    ]
    with conn.cursor() as cur:
        cur.executemany(_INSERT_SENTENCE, rows)
    conn.commit()