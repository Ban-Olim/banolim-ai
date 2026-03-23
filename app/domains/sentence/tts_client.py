# 문장분해 TTS: ElevenLabs로 텍스트 → 음성 → base64

import base64
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# .env 로드
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

# 젊은 여성 교사 voice_id
TEACHER_VOICE_ID = "xmO7mipIuizS5mxGvKtD"

# 레벨별 음성 설정 정의
LOW_AGE_VOICE_SETTINGS = VoiceSettings(
    stability=0.6,               # 목소리의 일관성 (높을수록 단정함)
    similarity_boost=0.75,        # 원본 목소리와의 유사도 (높을수록 원본과 비슷)
    style=0.5,                    # 감정 표현 정도 (0.0~1.0, 높을수록 감정적)
    use_speaker_boost=True        # 목소리 선명도 강화 
) #(7-10세)

HIGH_AGE_VOICE_SETTINGS = VoiceSettings(
    stability=0.7, 
    similarity_boost=0.80, 
    style=0.1, 
    use_speaker_boost=True
) #(11-13세, 좀 더 차분한 톤)
 
# ElevenLabs 클라이언트 생성
def _get_client() -> ElevenLabs:
    api_key = os.getenv("SENTENCE_ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("SENTENCE_ELEVENLABS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return ElevenLabs(api_key=api_key)

# 나이에 따른 음성 설정 반환
def _get_voice_settings(user_age: int):
    if user_age <= 10:   # (7-10세)
        return LOW_AGE_VOICE_SETTINGS
    else:
        return HIGH_AGE_VOICE_SETTINGS  # (11-13세)

# 레벨에 따른 음성 설정 사용

# 텍스트를 ElevenLabs로 음성 생성 후 base64 문자열로 반환
def text_to_speech_base64(text: str, voice_settings: VoiceSettings) -> Optional[str]:
    try:
        client = _get_client()

        # ElevenLabs는 음성 데이터를 '조각(Generator)' 단위로 전송
        audio_iterator = client.text_to_speech.convert(
            voice_id=TEACHER_VOICE_ID,
            text=text,
            voice_settings=voice_settings,
            model_id="eleven_multilingual_v2"
        )

        # 조각들을 하나로 합쳐 base64로 인코딩
        audio_data = b"".join(audio_iterator)
        
        if not audio_data:
            return None
        
        return base64.b64encode(audio_data).decode("utf-8")
    
    except Exception as e:
        print(f"TTS 생성 중 오류 발생: {e}")
        return None
    
def generate_sentence_audio_base64(text: str, user_age: int) -> Optional[str]:
    voice_settings = _get_voice_settings(user_age)
    return text_to_speech_base64(text, voice_settings)