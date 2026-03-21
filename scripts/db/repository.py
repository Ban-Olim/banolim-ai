
_INSERT_BOOK = """
INSERT INTO books (book_id, level)
VALUES (%s, %s)
ON CONFLICT (book_id) DO UPDATE SET
    level = EXCLUDED.level;
"""

_INSERT_SENTENCE = """
INSERT INTO sentences (book_id, level, idx, text)
VALUES (%s, %s, %s, %s)
ON CONFLICT (book_id, idx) DO UPDATE SET
    text = EXCLUDED.text;
"""

def upsert_book(conn, book_id: str, level: int):
    with conn.cursor() as cur:
        cur.execute(_INSERT_BOOK, (book_id, level))

def upsert_sentences(conn, book_id: str, level: int, sentences: list[str]):
    rows = [(book_id, level, idx, text) for idx, text in enumerate(sentences)]
    with conn.cursor() as cur:
        cur.executemany(_INSERT_SENTENCE, rows)
    conn.commit()