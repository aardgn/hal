
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

print("Ses yazıya çevriliyor...")

with open("hal_mic_test.wav", "rb") as audio_file:
    result = client.speech_to_text.convert(
        file=audio_file,
        model_id="scribe_v1",
        language_code="tur",
    )

print("Algılanan konuşma:")
print(result.text)
