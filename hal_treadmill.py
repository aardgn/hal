
import asyncio
import re
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

from openwakeword.model import Model
from elevenlabs.client import ElevenLabs
from bleak import BleakClient, BleakScanner
from dotenv import load_dotenv
import os

load_dotenv()

CONTROL_POINT = "00002ad9-0000-1000-8000-00805f9b34fb"
SAMPLE_RATE = 16000
RECORD_SECONDS = 4

client_ai = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def record_command():
    print("Dinliyorum, komutunu söyle...")
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    wav.write("hal_command.wav", SAMPLE_RATE, audio)
    return "hal_command.wav"


def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        result = client_ai.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1",
            language_code="tur",
        )

    text = getattr(result, "text", "")
    print("Duyduğum:", text)
    return text




def extract_speed(text):
    text = text.lower().replace(",", ".")

    number_words = {
        "bir": "1",
        "iki": "2",
        "üç": "3",
        "dört": "4",
        "dörde": "4",
        "beş": "5",
        "altı": "6",
        "yedi": "7",
        "sekiz": "8",
    }

    for word, digit in number_words.items():
        text = re.sub(rf"\b{word}\b", digit, text)

    # Sadece hız değiştirme niyeti içeren cümleleri kabul et
    has_speed = "hız" in text
    actions = [
        "çıkar", "artır", "arttir", "yükselt",
        "yap", "ayarla", "indir", "azalt", "düşür", "dusur"
    ]
    has_action = any(action in text for action in actions)

    if not has_speed or not has_action:
        return None

    match = re.search(r"(?<!\d)([1-8](?:\.\d)?)(?!\d)", text)

    if not match:
        return None

    speed = float(match.group(1))

    if not 1.0 <= speed <= 8.0:
        return None

    return speed




async def set_treadmill_speed(speed):
    print("Bluetooth cihazları aranıyor...")
    devices = await BleakScanner.discover(timeout=8)

    candidates = [
        device for device in devices
        if device.name and device.name.startswith("FS-")
    ]

    if not candidates:
        raise RuntimeError("Koşu bandı bulunamadı.")

    device = next(
        (d for d in candidates if d.name == "FS-613934"),
        candidates[0],
    )

    print(f"Bağlanılıyor: {device.name}")

    async with BleakClient(device) as ble:
        responses = asyncio.Queue()

        def on_control_point(sender, data):
            responses.put_nowait(bytes(data))

        await ble.start_notify(CONTROL_POINT, on_control_point)

        async def send_command(command):
            await ble.write_gatt_char(
                CONTROL_POINT, command, response=True
            )

            try:
                response = await asyncio.wait_for(
                    responses.get(), timeout=5
                )
            except asyncio.TimeoutError:
                raise RuntimeError("Cihazdan yanıt gelmedi.")

            print("Bluetooth yanıtı:", response.hex(" "))

            if (
                len(response) < 3
                or response[0] != 0x80
                or response[1] != command[0]
                or response[2] != 0x01
            ):
                raise RuntimeError("Komut cihaz tarafından onaylanmadı.")

        try:
            await send_command(bytes([0x00]))

            value = round(speed * 100)
            command = bytes([
                0x02,
                value & 0xFF,
                (value >> 8) & 0xFF,
            ])

            await send_command(command)
            print(f"Hız komutu onaylandı: {speed:.1f} km/sa")

        finally:
            await ble.stop_notify(CONTROL_POINT)


def main():
    print("Hey Jarvis dinleniyor. Çıkmak için Ctrl+C.")

    wake_model = Model(wakeword_models=["hey_jarvis"])

    with sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="int16",
        blocksize=1280,
    ) as stream:
        while True:
            audio, _ = stream.read(1280)
            prediction = wake_model.predict(np.squeeze(audio))

            if max(prediction.values(), default=0) > 0.5:
                print("\nHey Jarvis algılandı!")

                filename = record_command()
                spoken_text = transcribe_audio(filename)
                speed = extract_speed(spoken_text)

                if speed is None:
                    print("Hızı anlayamadım. Örneğin: 'hızı 4'e çıkar'.")
                    continue

                print(f"Hedef hız: {speed:.1f} km/sa")
                asyncio.run(set_treadmill_speed(speed))

                print("\nHey Jarvis dinleniyor...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nHal kapatıldı.")
