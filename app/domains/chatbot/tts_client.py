# 챗봇 TTS: ElevenLabs로 텍스트 → 음성 → base64

import base64
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from functools import lru_cache

# .env 로드
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

# 캐릭터 번호와 ElevenLabs voice_id 매핑
CHARACTER_VOICE_IDS = {
    1: "8jHHF8rMqMlg8if2mOUe",  # 정수아
    2: "Ml2fm7pJDDTZqQkeGpRM",  # 한지후 
    3: "zgDzx5jLLCqEp6Fl7Kl7",  # 김민지 
    4: "4JJwo477JUAx3HV0T7n7",  # 박성찬 
}

# ElevenLabs 클라이언트 생성
@lru_cache(maxsize=1)
def _get_client() -> ElevenLabs:
    api_key = os.getenv("CHATBOT_ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("CHATBOT_ELEVENLABS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return ElevenLabs(api_key=api_key)

#캐릭터 번호에 해당하는 voice_id 반환
def get_voice_id(character_id: int) -> str:
    return CHARACTER_VOICE_IDS.get(character_id, "")


# 텍스트를 ElevenLabs로 음성 생성 후 base64 문자열로 반환
# voice_id가 비어 있으면 None 반환
def text_to_speech_base64(text: str, voice_id: str) -> Optional[str]:
    if not text.strip() or not voice_id:
        return None
    client = _get_client()
    audio = client.text_to_speech.convert(voice_id=voice_id, text=text)
    # 스트림/이터레이터면 bytes로 합침
    if hasattr(audio, "__iter__") and not isinstance(audio, bytes):
        chunks = list(audio)
        data = b"".join(chunks) if chunks else b""
    else:
        data = bytes(audio) if not isinstance(audio, bytes) else audio
    return base64.b64encode(data).decode("utf-8") if data else None
