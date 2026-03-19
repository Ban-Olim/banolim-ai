EMBEDDING_DIM = 1536

_CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS vector;"

# books 테이블: 책 ID와 레벨 저장
_CREATE_BOOKS = """
CREATE TABLE IF NOT EXISTS books (
    book_id     VARCHAR PRIMARY KEY,
    level       INTEGER NOT NULL
);
"""

# sentences 테이블: 책 ID, 레벨, 문장 인덱스, 텍스트, 임베딩 저장
_CREATE_SENTENCES = f"""
CREATE TABLE IF NOT EXISTS sentences (
    id          SERIAL PRIMARY KEY,
    book_id     VARCHAR NOT NULL REFERENCES books(book_id),
    level       INTEGER NOT NULL,
    idx         INTEGER NOT NULL,
    text        TEXT    NOT NULL,
    embedding   vector({EMBEDDING_DIM}),

    UNIQUE (book_id, idx)
);
"""

# sentences 테이블의 임베딩 컬럼에 대한 벡터 인덱스 생성
_CREATE_SENTENCES_INDEX = """
CREATE INDEX IF NOT EXISTS sentences_embedding_idx
ON sentences
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 10);
"""

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(_CREATE_EXTENSION)
        cur.execute(_CREATE_BOOKS)
        cur.execute(_CREATE_SENTENCES)
        cur.execute(_CREATE_SENTENCES_INDEX)
    conn.commit()
    print("DB 초기화 완료 (extension / books / sentences / index)")