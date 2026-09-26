from tts.tts_engine import text_to_speech
from semantic.packet_schema import SemanticPacket
from communication.semantic_transport import transmit_semantic_packet


def _hindi_object(object_name):
    """
    Convert semantic object labels into Hindi.
    """

    translations = {
        "MEDICINE": "दवाई",
        "WATER": "पानी",
        "FOOD": "खाना",
        "FUEL": "ईंधन",
        "BLOOD": "खून",
        "EQUIPMENT": "उपकरण",
    }

    return translations.get(
        object_name,
        object_name
    )


def semantic_decode(packet: SemanticPacket):
    """
    Convert the recovered semantic packet
    into natural language.

    Supports English and Hindi.
    """

    # -------------------------
    # HINDI
    # -------------------------

    if packet.language == "hi":

        sector = packet.location.replace(
            "SECTOR_",
            ""
        )

        if packet.intent == "SUPPLY_REQUEST":
            return (
                f"सेक्टर {sector} में "
                f"{_hindi_object(packet.object)} भेजें।"
            )

        if packet.intent == "ALERT":
            return (
                f"सेक्टर {sector} में "
                f"{_hindi_object(packet.object)} "
                f"के लिए चेतावनी।"
            )

        return (
            f"सेक्टर {sector} में "
            f"{_hindi_object(packet.object)}।"
        )

    # -------------------------
    # ENGLISH
    # -------------------------

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

    English and Hindi use different TTS voices
    based on packet.language.
    """

    # -------------------------
    # TRANSMISSION
    # -------------------------

    result = transmit_semantic_packet(
        packet,
        snr_db=10
    )

    # -------------------------
    # TRANSMISSION FAILURE
    # -------------------------

    if not result["success"]:

        print("Transmission failed.")
        print("CRC: INVALID")

        return None, None, result

    # -------------------------
    # RECOVERED PACKET
    # -------------------------

    recovered_packet = result["packet"]

    # -------------------------
    # SEMANTIC DECODING
    # -------------------------

    text = semantic_decode(
        recovered_packet
    )

    print("Recovered message:")
    print(text)

    print(
        f"Recovered language: "
        f"{recovered_packet.language}"
    )

    # -------------------------
    # LANGUAGE-AWARE TTS
    # -------------------------

    audio_file = text_to_speech(
        text,
        language=recovered_packet.language
    )

    return text, audio_file, result


if __name__ == "__main__":

    # -------------------------
    # ENGLISH TEST PACKET
    # -------------------------

    english_packet = SemanticPacket(
        version=1,
        language="en",
        intent="SUPPLY_REQUEST",
        object="MEDICINE",
        location="SECTOR_4",
        priority="HIGH"
    )

    print("=" * 60)
    print("ENGLISH TRANSMISSION TEST")
    print("=" * 60)

    text, audio, result = receiver(
        english_packet
    )

    if result["success"]:

        print(
            f"Recovered English text: "
            f"{text}"
        )

        print(
            f"Audio generated: "
            f"{audio}"
        )

        print(
            "CRC: VALID"
        )


    # -------------------------
    # HINDI TEST PACKET
    # -------------------------

    hindi_packet = SemanticPacket(
        version=1,
        language="hi",
        intent="SUPPLY_REQUEST",
        object="WATER",
        location="SECTOR_7",
        priority="HIGH"
    )

    print()
    print("=" * 60)
    print("HINDI TRANSMISSION TEST")
    print("=" * 60)

    text, audio, result = receiver(
        hindi_packet
    )

    if result["success"]:

        print(
            f"Recovered Hindi text: "
            f"{text}"
        )

        print(
            f"Audio generated: "
            f"{audio}"
        )

        print(
            "CRC: VALID"
        )