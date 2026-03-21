_CREATE_BOOKS = """
CREATE TABLE IF NOT EXISTS books (
    book_id     VARCHAR PRIMARY KEY,
    level       INTEGER NOT NULL
);
"""

_CREATE_SENTENCES = """
CREATE TABLE IF NOT EXISTS sentences (
    id          SERIAL PRIMARY KEY,
    book_id     VARCHAR NOT NULL REFERENCES books(book_id),
    level       INTEGER NOT NULL,
    idx         INTEGER NOT NULL,
    text        TEXT    NOT NULL,

    UNIQUE (book_id, idx)
);
"""

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(_CREATE_BOOKS)
        cur.execute(_CREATE_SENTENCES)
    conn.commit()
    print("DB 초기화 완료 (books / sentences)")