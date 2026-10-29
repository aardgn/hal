
import openwakeword
import sounddevice as sd
import numpy as np
from openwakeword.model import Model

openwakeword.utils.download_models()

model = Model(wakeword_models=["hey_jarvis"])

print("Hal dinliyor... 'Hey Jarvis' de. Çıkmak için Ctrl+C.")

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="int16",
    blocksize=1280,
) as stream:
    while True:
        audio, overflowed = stream.read(1280)
        audio = np.squeeze(audio)
        prediction = model.predict(audio)

        for name, score in prediction.items():
            if score > 0.5:
                print(f"Uyandırma algılandı: {name} ({score:.2f})")
