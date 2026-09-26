from pathlib import Path
import wave

from piper.voice import PiperVoice


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "tts" / "models"

MODELS = {
    "en": MODEL_DIR / "en_US-lessac-medium.onnx",
    "hi": MODEL_DIR / "hi_IN-priyamvada-medium.onnx",
}

_voices = {}


def get_voice(language):
    language = language.lower()

    if language not in MODELS:
        language = "en"

    if language not in _voices:
        model_path = MODELS[language]

        if not model_path.exists():
            raise FileNotFoundError(
                f"Piper model not found: {model_path}"
            )

        _voices[language] = PiperVoice.load(str(model_path))

    return _voices[language]


def text_to_speech(text, language="en", output_file=None):
    language = language.lower()

    if language not in MODELS:
        language = "en"

    if output_file is None:
        output_file = PROJECT_ROOT / f"output_{language}.wav"
    else:
        output_file = Path(output_file)

    voice = get_voice(language)

    with wave.open(str(output_file), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    if not output_file.exists() or output_file.stat().st_size == 0:
        raise RuntimeError("Piper produced an empty audio file.")

    return output_file


if __name__ == "__main__":
    english_file = text_to_speech(
        "Send medical supplies to sector four immediately.",
        language="en",
    )
    print(f"English audio generated: {english_file}")

    hindi_file = text_to_speech(
        "सेक्टर चार में तुरंत चिकित्सा सामग्री भेजें।",
        language="hi",
    )
    print(f"Hindi audio generated: {hindi_file}")