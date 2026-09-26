import asyncio
import edge_tts


async def generate_speech(text, output_file="output.mp3"):
    voice = "en-US-AriaNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def text_to_speech(text, output_file="output.mp3"):
    asyncio.run(generate_speech(text, output_file))


if __name__ == "__main__":
    text_to_speech(
        "Send medical supplies to sector four immediately."
    )

    print("Speech generated successfully.")