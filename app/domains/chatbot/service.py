# 챗봇 비즈니스 로직: 프롬프트 조립 → LLM 호출 → TTS → 응답 반환

from . import client, prompt_builder, tts_client
from .schemas import ChatbotRequest, ChatbotResponse


def chat(req: ChatbotRequest) -> ChatbotResponse:
    try:
       # 1. 프롬프트 및 메시지 준비
        system_prompt = prompt_builder.build_system_prompt(
            character_id=req.character_id,
            user_name=req.user_name,
            user_age=req.user_age,
            current_temperature=req.current_temperature
        )

        messages = [
            {"role": "assistant" if m.role == "BOT" else "user", "content": m.content}
            for m in req.messages
        ]
        
        # 2. LLM(OpenAI) 호출
        result = client.generate(system_prompt, messages)
    
        # 증감은 무조건 -3 또는 +5만 적용 (0이어도 +5)
        current = req.current_temperature
        delta = result["temperature"] - current
        if delta < 0:
            delta = -3
        else:
            delta = 5
        new_temperature = max(0, min(100, current + delta))

        # TTS: 답변 텍스트 → 캐릭터 voice_id로 음성 생성 → base64
        voice_id = tts_client.get_voice_id(req.character_id)
        audio_base64 = tts_client.text_to_speech_base64(result["message"], voice_id)

        return ChatbotResponse(
            message=result["message"],
            temperature=new_temperature,
            audio_base64=audio_base64,
        )
       
    except Exception:
        # 에러가 발생하면 무조건 아래의 안내 문구와 기존 온도를 반환함
        return ChatbotResponse(
            message="서버에 요청이 너무 많습니다! 잠시 뒤, 다시 시도해주세요!",
            temperature=req.current_temperature,
            audio_base64=""
        )
