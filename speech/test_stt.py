from speech.stt_engine import speech_to_text


AUDIO_FILE = "english_test.mp3"

result = speech_to_text(AUDIO_FILE)

print("=" * 60)
print("STT TEST")
print("=" * 60)

print("Detected language:", result["language"])
print(
    "Language probability:",
    f'{result["language_probability"]:.2f}'
)

print("Transcript:")
print(result["text"])