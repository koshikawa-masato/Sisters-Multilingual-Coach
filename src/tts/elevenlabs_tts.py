"""
ElevenLabs TTS Provider for Sisters-Multilingual-Coach
"""

import os
from typing import Optional
from elevenlabs import ElevenLabs, Voice, VoiceSettings


class ElevenLabsTTS:
    """Text-to-Speech using ElevenLabs API"""

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not set in environment")

        self.client = ElevenLabs(api_key=self.api_key)

        # Voice IDs for each sister (can be customized)
        self.voice_ids = {
            "Botan": os.getenv("ELEVENLABS_VOICE_ID_BOTAN", "21m00Tcm4TlvDq8ikWAM"),  # Rachel
            "Kasho": os.getenv("ELEVENLABS_VOICE_ID_KASHO", "AZnzlk1XvdvUeBnXmlld"),  # Domi
            "Yuri": os.getenv("ELEVENLABS_VOICE_ID_YURI", "EXAVITQu4vr4xnSDxMaL"),   # Bella
        }

        self.model = os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2")

    def generate_speech(
        self,
        text: str,
        sister: str = "Botan",
        output_path: Optional[str] = None
    ) -> bytes:
        """
        Generate speech from text using ElevenLabs

        Args:
            text: Text to convert to speech
            sister: Which sister's voice to use (Botan, Kasho, Yuri)
            output_path: Optional path to save audio file

        Returns:
            Audio data as bytes
        """
        voice_id = self.voice_ids.get(sister, self.voice_ids["Botan"])

        # Generate audio
        audio = self.client.generate(
            text=text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.5,
                    use_speaker_boost=True
                )
            ),
            model=self.model
        )

        # Convert generator to bytes
        audio_bytes = b"".join(audio)

        # Save to file if path provided
        if output_path:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        return audio_bytes

    def get_available_voices(self) -> list:
        """Get list of available voices from ElevenLabs"""
        voices = self.client.voices.get_all()
        return [{"id": v.voice_id, "name": v.name} for v in voices.voices]
