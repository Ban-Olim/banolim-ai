from db.repository import upsert_book, upsert_sentences
from schemas import BookData

from .client import get_embeddings#

# 책 데이터 → 임베딩 생성 → DB 저장
def embed_and_store(conn, data: BookData) -> int:
    sentences = data.sentences
    if not sentences:
        print("문장 없음, 스킵")
        return 0

    upsert_book(conn, data.book_id, data.level)
    embeddings = get_embeddings(sentences)
    upsert_sentences(conn, data.book_id, data.level, sentences, embeddings)
    return len(sentences)
