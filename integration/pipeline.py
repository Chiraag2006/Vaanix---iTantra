from tts.tts_engine import text_to_speech
from semantic.packet_schema import SemanticPacket
from communication.semantic_transport import transmit_semantic_packet


def semantic_decode(packet: SemanticPacket):
    """
    Convert the recovered semantic packet into natural language.
    """

    if packet.intent == "SUPPLY_REQUEST":
        return (
            f"Send {packet.object.lower()} "
            f"to {packet.location.replace('_', ' ').lower()}."
        )

    if packet.intent == "ALERT":
        return (
            f"Alert: {packet.object.lower()} "
            f"at {packet.location.replace('_', ' ').lower()}."
        )

    return (
        f"{packet.intent.replace('_', ' ').title()}: "
        f"{packet.object.lower()} "
        f"at {packet.location.replace('_', ' ').lower()}."
    )


def receiver(packet: SemanticPacket):
    """
    Transmit a semantic packet through the complete
    communication chain and reconstruct speech.
    """

    result = transmit_semantic_packet(packet)

    if not result["success"]:
        return None, None, result

    recovered_packet = result["packet"]

    text = semantic_decode(
        recovered_packet
    )

    print("Recovered message:")
    print(text)

    audio_file = text_to_speech(
        text
    )

    return text, audio_file, result


if __name__ == "__main__":

    packet = SemanticPacket(
        version=1,
        language="en",
        intent="SUPPLY_REQUEST",
        object="MEDICINE",
        location="SECTOR_4",
        priority="HIGH"
    )

    text, audio, result = receiver(packet)

    if result["success"]:
        print(f"Recovered text: {text}")
        print(f"Audio generated: {audio}")
        print("CRC: VALID")
    else:
        print("Transmission failed.")
        print("CRC: INVALID")