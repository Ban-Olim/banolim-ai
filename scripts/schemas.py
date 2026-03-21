from pydantic import BaseModel

class BookData(BaseModel):
    book_id: str
    level: int
    title: str
    total_sentences: int
    sentences: list[str]
