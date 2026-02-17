from . import client, prompt_builder
from .schemas import WordbookRequest, WordbookResponse

def generate_example(req: WordbookRequest) -> WordbookResponse:
    system_prompt = prompt_builder.build_system_prompt()
    user_prompt = prompt_builder.build_user_prompt(req.lemma, req.definition, req.pos)

    # 단순한 구조이므로 messages 리스트를 여기서 바로 생성
    messages = [
        {"role": "user", "content": user_prompt}
    ]

    result = client.generate(system_prompt, messages)

    return WordbookResponse(
        example_sentence=result["example_sentence"],
        translation=result["translation"]
    )
