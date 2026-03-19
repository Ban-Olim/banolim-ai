from fastapi import APIRouter
from .schemas import WordbookRequest, WordbookResponse
from . import service

router = APIRouter(prefix="/wordbook", tags=["wordbook"])

@router.post("/example-sentences", response_model=WordbookResponse)
def generate_example(body: WordbookRequest) -> WordbookResponse:
    return service.generate_example(body)
