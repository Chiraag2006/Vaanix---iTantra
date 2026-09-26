from tts.tts_engine import text_to_speech
from semantic.packet_schema import SemanticPacket


def semantic_decode(packet: SemanticPacket):
    return (
        f"Send {packet.object.lower()} "
        f"to {packet.location.replace('_', ' ').lower()}."
    )


def receiver(packet: SemanticPacket):

    text = semantic_decode(packet)

    print("Recovered message:")
    print(text)

    text_to_speech(text)

    return text


if __name__ == "__main__":

    packet = SemanticPacket(
        version=1,
        language="en",
        intent="SUPPLY_REQUEST",
        object="MEDICINE",
        location="SECTOR_4",
        priority="HIGH"
    )

    receiver(packet)