import os

from openai import OpenAI

_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

MODEL = "text-embedding-3-small"
BATCH_SIZE = 50

# 텍스트 리스트 → 임베딩 리스트
def get_embeddings(texts: list[str]) -> list[list[float]]:
    embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = _client.embeddings.create(model=MODEL, input=batch)
        embeddings.extend(item.embedding for item in response.data)
    return embeddings
