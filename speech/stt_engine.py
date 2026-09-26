from faster_whisper import WhisperModel


# --------------------------------------------------
# MODEL CONFIGURATION
# --------------------------------------------------

MODEL_SIZE = "small"

_model = None


def get_model():
    """
    Load the Whisper model once and reuse it.
    """
    global _model

    if _model is None:
        _model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    return _model


def speech_to_text(audio_file):
    """
    Transcribe an audio file.

    Returns:
        {
            "text": "...",
            "language": "en" or "hi",
            "language_probability": float
        }
    """

    model = get_model()

    segments, info = model.transcribe(
        audio_file,
        beam_size=5,
        vad_filter=True
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    language = info.language

    return {
        "text": text,
        "language": language,
        "language_probability": info.language_probability
    }


if __name__ == "__main__":
    print("Whisper STT engine ready.")
    print(f"Model: {MODEL_SIZE}")
    print("Supported demo languages: English + Hindi")