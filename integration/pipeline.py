from tts.tts_engine import text_to_speech


def semantic_decode(packet):
    """
    Temporary decoder.
    This will later be replaced by the real
    semantic decoder from Member 2.
    """

    return (
        f"Send {packet['object'].lower()} "
        f"to {packet['location'].replace('_', ' ').lower()}."
    )


def receiver(packet):
    text = semantic_decode(packet)

    print("Recovered message:")
    print(text)

    text_to_speech(text)

    return text


if __name__ == "__main__":

    packet = {
        "object": "MEDICINE",
        "location": "SECTOR_4"
    }

    receiver(packet)