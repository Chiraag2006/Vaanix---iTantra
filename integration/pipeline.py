from tts.tts_engine import text_to_speech
from semantic.packet_schema import SemanticPacket


def semantic_decode(packet: SemanticPacket):

    """
    Temporary semantic decoder.

    This will later be replaced by the
    actual decoder from the semantic/channel team.
    """

    return (
        f"Send {packet.object.lower()} "
        f"to {packet.location.replace('_', ' ').lower()}."
    )


def receiver(packet: SemanticPacket):

    text = semantic_decode(packet)

    print("Recovered message:")
    print(text)

    audio_file = text_to_speech(text)

    return text, audio_file


if __name__ == "__main__":

    packet = SemanticPacket(
        version=1,
        language="en",
        intent="SUPPLY_REQUEST",
        object="MEDICINE",
        location="SECTOR_4",
        priority="HIGH"
    )

    text, audio = receiver(packet)

    print(f"Audio generated: {audio}")