from tts.tts_engine import text_to_speech
from semantic.packet_schema import SemanticPacket
from communication.semantic_transport import transmit_semantic_packet


def _hindi_object(object_name):
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
        object_name,
    )


def semantic_decode(packet: SemanticPacket):

    # -------------------------------------------------
    # FREE / GENERAL MESSAGE
    # -------------------------------------------------

    # If the original message was preserved,
    # return it instead of inventing a new sentence.
    if packet.message:
        return packet.message

    # -------------------------------------------------
    # STRUCTURED HINDI MESSAGE
    # -------------------------------------------------

    if packet.language == "hi":

        sector = packet.location.replace(
            "SECTOR_",
            "",
        )

        object_name = _hindi_object(
            packet.object
        )

        if packet.intent == "SUPPLY_REQUEST":

            if packet.location != "UNKNOWN":
                return (
                    f"सेक्टर {sector} में "
                    f"{object_name} भेजें।"
                )

            return f"{object_name} भेजें।"

        if packet.intent == "ALERT":

            if packet.location != "UNKNOWN":
                return (
                    f"सेक्टर {sector} में "
                    f"{object_name} के लिए चेतावनी।"
                )

            return f"{object_name} के लिए चेतावनी।"

        return (
            f"{packet.intent.replace('_', ' ').title()}: "
            f"{object_name}"
        )

    # -------------------------------------------------
    # STRUCTURED ENGLISH MESSAGE
    # -------------------------------------------------

    if packet.intent == "SUPPLY_REQUEST":

        object_name = packet.object.lower()

        if packet.location != "UNKNOWN":
            location = (
                packet.location
                .replace("_", " ")
                .lower()
            )

            return (
                f"Send {object_name} "
                f"to {location}."
            )

        return f"Send {object_name}."

    if packet.intent == "ALERT":

        object_name = packet.object.lower()

        if packet.location != "UNKNOWN":
            location = (
                packet.location
                .replace("_", " ")
                .lower()
            )

            return (
                f"Alert: {object_name} "
                f"at {location}."
            )

        return f"Alert: {object_name}."

    return (
        f"{packet.intent.replace('_', ' ').title()}: "
        f"{packet.object.lower()}"
    )


def receiver(packet: SemanticPacket):

    result = transmit_semantic_packet(
        packet,
        snr_db=10,
    )

    if not result["success"]:

        print("Transmission failed.")
        print("CRC: INVALID")

        return None, None, result

    recovered_packet = result["packet"]

    text = semantic_decode(
        recovered_packet
    )

    print("Recovered message:")
    print(text)

    print(
        f"Recovered language: "
        f"{recovered_packet.language}"
    )

    audio_file = text_to_speech(
        text,
        language=recovered_packet.language,
    )

    return text, audio_file, result


if __name__ == "__main__":

    english_packet = SemanticPacket(
        version=1,
        language="en",
        intent="SUPPLY_REQUEST",
        object="MEDICINE",
        location="SECTOR_4",
        priority="HIGH",
        message="",
    )

    print("=" * 60)
    print("ENGLISH TRANSMISSION TEST")
    print("=" * 60)

    text, audio, result = receiver(
        english_packet
    )

    if result["success"]:

        print(
            f"Recovered English text: {text}"
        )

        print(
            f"Audio generated: {audio}"
        )

        print("CRC: VALID")


    hindi_packet = SemanticPacket(
        version=1,
        language="hi",
        intent="SUPPLY_REQUEST",
        object="WATER",
        location="SECTOR_7",
        priority="HIGH",
        message="",
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
            f"Recovered Hindi text: {text}"
        )

        print(
            f"Audio generated: {audio}"
        )

        print("CRC: VALID")