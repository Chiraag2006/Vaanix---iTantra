import re

from semantic.packet_schema import SemanticPacket


NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


HINDI_NUMBER_WORDS = {
    "शून्य": 0,
    "एक": 1,
    "दो": 2,
    "तीन": 3,
    "चार": 4,
    "पाँच": 5,
    "पांच": 5,
    "छह": 6,
    "सात": 7,
    "आठ": 8,
    "नौ": 9,
    "दस": 10,
}


def detect_language(text):
    """
    Detect Hindi or English from the text.

    Devanagari characters -> Hindi
    Otherwise -> English
    """

    if re.search(r"[\u0900-\u097F]", text):
        return "hi"

    return "en"


def extract_location(text):
    """
    Extract sector number from English or Hindi text.
    """

    text_lower = text.lower()

    # English numeric sector
    match = re.search(
        r"sector\s+(\d+)",
        text_lower
    )

    if match:
        return f"SECTOR_{match.group(1)}"

    # English number word
    for word, number in NUMBER_WORDS.items():

        if re.search(
            rf"sector\s+{word}",
            text_lower
        ):
            return f"SECTOR_{number}"

    # Hindi numeric sector
    match = re.search(
        r"सेक्टर\s+(\d+)",
        text
    )

    if match:
        return f"SECTOR_{match.group(1)}"

    # Hindi number word
    for word, number in HINDI_NUMBER_WORDS.items():

        if re.search(
            rf"सेक्टर\s+{word}",
            text
        ):
            return f"SECTOR_{number}"

    return "UNKNOWN"


def extract_object(text):
    """
    Detect the main supply object.
    Supports English and Hindi.
    """

    text_lower = text.lower()

    objects = [
        (
            "MEDICINE",
            [
                "medicine",
                "medicines",
                "medical supplies",
                "दवा",
                "दवाइयाँ",
                "दवाएं",
                "चिकित्सा सामग्री",
            ]
        ),
        (
            "WATER",
            [
                "water",
                "water supplies",
                "पानी",
                "जल",
            ]
        ),
        (
            "FOOD",
            [
                "food",
                "food supplies",
                "भोजन",
                "खाना",
            ]
        ),
        (
            "FUEL",
            [
                "fuel",
                "ईंधन",
            ]
        ),
        (
            "BLOOD",
            [
                "blood",
                "रक्त",
                "खून",
            ]
        ),
        (
            "EQUIPMENT",
            [
                "equipment",
                "उपकरण",
                "सामान",
            ]
        ),
    ]

    for object_name, keywords in objects:

        for keyword in keywords:

            if keyword in text_lower:
                return object_name

    return "UNKNOWN"


def extract_priority(text):
    """
    Determine message priority in English or Hindi.
    """

    text_lower = text.lower()

    high_priority_words = [
        # English
        "urgent",
        "urgently",
        "immediately",
        "emergency",
        "critical",
        "asap",

        # Hindi
        "तुरंत",
        "आपातकाल",
        "आपात",
        "जरूरी",
        "अत्यावश्यक",
        "तत्काल",
    ]

    for word in high_priority_words:

        if word in text_lower:
            return "HIGH"

    return "NORMAL"


def extract_intent(text):
    """
    Detect message intent in English or Hindi.
    """

    text_lower = text.lower()

    # ALERT
    alert_words = [
        "alert",
        "warning",
        "danger",
        "emergency",
        "चेतावनी",
        "खतरा",
        "आपातकाल",
        "आपात",
    ]

    if any(
        phrase in text_lower
        for phrase in alert_words
    ):
        return "ALERT"

    # SUPPLY REQUEST
    supply_words = [
        "send",
        "deliver",
        "supply",
        "supplies",
        "provide",

        "भेजो",
        "भेजें",
        "भेजना",
        "पहुंचाओ",
        "पहुँचाओ",
        "आपूर्ति",
        "आपूर्ति भेजो",
        "उपलब्ध कराओ",
    ]

    if any(
        phrase in text_lower
        for phrase in supply_words
    ):
        return "SUPPLY_REQUEST"

    return "GENERAL_MESSAGE"


def encode_message(text):
    """
    Convert English or Hindi natural-language text
    into a semantic packet.
    """

    text = text.strip()

    language = detect_language(text)

    location = extract_location(text)
    object_name = extract_object(text)
    priority = extract_priority(text)
    intent = extract_intent(text)

    return SemanticPacket(
        version=1,
        language=language,
        intent=intent,
        object=object_name,
        location=location,
        priority=priority,
    )


if __name__ == "__main__":

    examples = [
        "Send medical supplies to sector four immediately.",
        "Send water supplies to sector seven immediately.",
        "Deliver food to sector two.",
        "Emergency fuel required at sector five.",

        "सेक्टर सात में तुरंत पानी की आपूर्ति भेजो।",
        "सेक्टर चार में तुरंत चिकित्सा सामग्री भेजें।",
        "सेक्टर दो में भोजन भेजो।",
        "सेक्टर पाँच में ईंधन की आपात आवश्यकता है।",
    ]

    for message in examples:

        packet = encode_message(message)

        print("\nMessage:")
        print(message)

        print("Language:")
        print(packet.language)

        print("Semantic packet:")
        print(packet)