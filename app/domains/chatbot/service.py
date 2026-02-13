# 챗봇 비즈니스 로직: 프롬프트 조립 → LLM 호출 → TTS → 응답 반환

from . import client, prompt_builder, tts_client
from .schemas import ChatbotRequest, ChatbotResponse


def chat(req: ChatbotRequest) -> ChatbotResponse:

    system_prompt = prompt_builder.build_system_prompt(
        character_id=req.character_id,
        user_name=req.user_name,
        user_age=req.user_age,
        current_temperature=req.current_temperature,
    )

    # ERD: USER / BOT → OpenAI: user / assistant
    messages = [
        {"role": "assistant" if m.role == "BOT" else "user", "content": m.content}
        for m in req.messages
    ]

    result = client.generate(system_prompt, messages)

    # TTS: 답변 텍스트 → 캐릭터 voice_id로 음성 생성 → base64
    voice_id = tts_client.get_voice_id(req.character_id)
    audio_base64 = tts_client.text_to_speech_base64(result["message"], voice_id)

    return ChatbotResponse(
        message=result["message"],
        temperature=result["temperature"],
        audio_base64=audio_base64,
    )
