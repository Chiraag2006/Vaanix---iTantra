import asyncio
from pathlib import Path

import edge_tts


# Project root:
# Vaanix---iTantra/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Generated audio file
DEFAULT_OUTPUT = PROJECT_ROOT / "output.mp3"


async def generate_speech(
    text,
    output_file=DEFAULT_OUTPUT
):
    voice = "en-US-AriaNeural"

    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(
        str(output_file)
    )


def text_to_speech(
    text,
    output_file=DEFAULT_OUTPUT
):
    asyncio.run(
        generate_speech(
            text,
            output_file
        )
    )

    return Path(output_file)


if __name__ == "__main__":

    output = text_to_speech(
        "Send medical supplies to sector four immediately."
    )

    print(
        f"Speech generated: {output}"
    )