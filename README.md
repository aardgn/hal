# Hal 🎙️🏃

**A voice-controlled treadmill assistant for macOS.**

Hal lets you control a compatible treadmill using natural language. Say *"Hey Jarvis, set the speed to 5"* and Hal listens to your command, transcribes your speech, and sends the speed adjustment over Bluetooth Low Energy (BLE).

## 💡 Why I Built This

Adjusting treadmill speed manually with the console can be a little tedious when all you want to do is speed up or slow down. I wanted a quicker, hands-free way to control the treadmill using voice commands.

I also built Hal as a small weekend project to get hands-on experience with **Speech-to-Text (STT), Text-to-Speech (TTS), wake-word detection, and Bluetooth device control**.

The goal was to combine these technologies into something practical that I could actually use in everyday life, rather than building another standalone AI demo.

## ✨ Features

- **Wake-word detection:** Activate the assistant by saying "Hey Jarvis".
- **Speech-to-Text:** Transcribe spoken commands in Turkish using ElevenLabs.
- **Natural-language commands:** Set treadmill speed using phrases such as "Hızı 5 yap" or "Hızı 4'e çıkar".
- **Bluetooth Low Energy:** Send speed adjustment commands directly to the treadmill.
- **Speed validation:** Validate requested speeds against the supported range of 1.0–8.0 km/h, in 0.1 km/h increments.

## 🛠️ Tech Stack

- Python
- [ElevenLabs](https://elevenlabs.io/) — Speech-to-Text and Text-to-Speech experiments
- [openWakeWord](https://github.com/dscripka/openWakeWord) — Wake-word detection
- [Bleak](https://github.com/hbldh/bleak) — Bluetooth Low Energy communication
- [SoundDevice](https://python-sounddevice.readthedocs.io/) — Microphone audio capture
- NumPy and SciPy — Audio processing

## ⚙️ Requirements

- macOS with a working microphone and Bluetooth
- Python 3.11 or another Python version compatible with the project's dependencies
- A compatible Bluetooth treadmill
- An ElevenLabs API key
- FFmpeg and PortAudio installed on your system

## 🙏 Acknowledgments

The Bluetooth communication implementation was developed using the FitShow/FTMS protocol information documented in [fitshow-treadmill-accessible](https://github.com/aradix85/fitshow-treadmill-accessible).

Hal adds wake-word detection and voice-command processing to enable hands-free treadmill speed control.

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/aardgn/hal.git
cd hal
```

Replace `aardgn/hal` with your repository's actual URL.

### 2. Install system dependencies

Using Homebrew:

```bash
brew install ffmpeg portaudio
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Python dependencies

Install the packages used by the project:

```bash
pip install bleak openwakeword sounddevice numpy scipy python-dotenv elevenlabs
```

Depending on your Python and macOS setup, you may need additional system dependencies for audio processing.

### 5. Configure your API key

Create a `.env` file in the project root:

```env
ELEVENLABS_API_KEY=your_api_key_here
```

Keep your API key private. Never commit your `.env` file to GitHub.

Make sure `.env` is listed in `.gitignore`.

### 6. Run Hal

```bash
python hal_treadmill.py
```

Say **"Hey Jarvis"**, then speak a supported command in Turkish.

Examples:

- "Hızı 4 yap."
- "Hızı 5'e çıkar."
- "Hızı 3'e ayarla."

## 🏃 Device Compatibility

Hal was developed and tested with a **POBO KB800 treadmill** using a FitShow-compatible Bluetooth module.

The implementation uses the Fitness Machine Service Control Point UUID:

`00002ad9-0000-1000-8000-00805f9b34fb`

Compatibility with other treadmill brands and models has not been verified. Bluetooth support alone does not guarantee that a treadmill supports remote speed control. Different devices may use different protocols or restrict remote control.

## ⚠️ Safety Notes

- Hal does not start the treadmill; the treadmill must be started manually.
- Test commands carefully and keep the emergency stop accessible.
- Voice recognition can misinterpret speech or background noise. Do not rely on it as a safety-critical control system.
- Check the target speed before testing and use the treadmill according to its manufacturer's instructions.

## 🔮 Possible Improvements

This is a small personal project, so the focus is on keeping it simple. Some possible future improvements include:

- Relative speed commands, such as "speed up a little" or "slow down".
- Better filtering of unintended voice commands.
- Spoken feedback after a successful speed adjustment.
- Testing compatibility with additional FTMS-enabled treadmills.

## 📄 License

This project is open source. A license has not yet been selected.
