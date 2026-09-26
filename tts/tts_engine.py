import asyncio
from pathlib import Path

import edge_tts


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output.mp3"


VOICES = {
    "en": "en-US-AriaNeural",
    "hi": "hi-IN-SwaraNeural",
}


async def generate_speech(
    text,
    language="en",
    output_file=DEFAULT_OUTPUT
):
    voice = VOICES.get(
        language,
        VOICES["en"]
    )

    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(
        str(output_file)
    )


def text_to_speech(
    text,
    language="en",
    output_file=DEFAULT_OUTPUT
):
    asyncio.run(
        generate_speech(
            text,
            language,
            output_file
        )
    )

    return Path(output_file)


if __name__ == "__main__":

    print("Testing English TTS...")

    english_output = text_to_speech(
        "Send water supplies to sector seven immediately.",
        language="en"
    )

    print(f"English audio: {english_output}")

    print("\nTesting Hindi TTS...")

    hindi_output = text_to_speech(
        "सेक्टर 7 में पानी भेजें",
        language="hi"
    )

    print(f"Hindi audio: {hindi_output}")