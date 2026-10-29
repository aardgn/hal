
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise ValueError(".env dosyasında API key bulunamadı.")

client = ElevenLabs(api_key=api_key)

audio = client.text_to_speech.convert(
    text="Merhaba. Ben Hal. Seni dinlemeye hazırım.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)
