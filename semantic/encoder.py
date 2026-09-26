
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
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"

    return "en"


def extract_location(text):
    text_lower = text.lower()

    # Numeric English sector
    match = re.search(r"sector\s+(\d+)", text_lower)

    if match:
        return f"SECTOR_{match.group(1)}"

    # English number-word sector
    for word, number in NUMBER_WORDS.items():
        if re.search(rf"sector\s+{word}", text_lower):
            return f"SECTOR_{number}"

    # Numeric Hindi sector
    match = re.search(r"सेक्टर\s+(\d+)", text)

    if match:
        return f"SECTOR_{match.group(1)}"

    # Hindi number-word sector
    for word, number in HINDI_NUMBER_WORDS.items():
        if re.search(rf"सेक्टर\s+{word}", text):
            return f"SECTOR_{number}"

    return "UNKNOWN"


def extract_object(text):
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
            ],
        ),
        (
            "WATER",
            [
                "water",
                "water supplies",
                "पानी",
                "जल",
            ],
        ),
        (
            "FOOD",
            [
                "food",
                "food supplies",
                "भोजन",
                "खाना",
            ],
        ),
        (
            "FUEL",
            [
                "fuel",
                "ईंधन",
            ],
        ),
        (
            "BLOOD",
            [
                "blood",
                "रक्त",
                "खून",
            ],
        ),
        (
            "EQUIPMENT",
            [
                "equipment",
                "उपकरण",
                "सामान",
            ],
        ),
        (
            "AMBULANCE",
            [
                "ambulance",
                "ambulances",
                "एम्बुलेंस",
                "एम्बुलन्स",
            ],
        ),
        (
            "HOSPITAL",
            [
                "hospital",
                "hospitals",
                "अस्पताल",
            ],
        ),
    ]

    for object_name, keywords in objects:
        for keyword in keywords:
            if keyword in text_lower:
                return object_name

    return "UNKNOWN"


def extract_priority(text):
    text_lower = text.lower()

    high_priority_words = [
        "urgent",
        "urgently",
        "immediately",
        "emergency",
        "critical",
        "asap",
        "help me",
        "help",
        "तुरंत",
        "आपातकाल",
        "आपात",
        "जरूरी",
        "अत्यावश्यक",
        "तत्काल",
        "मदद",
        "बचाओ",
    ]

    for word in high_priority_words:
        if word in text_lower:
            return "HIGH"

    return "NORMAL"


def extract_intent(text):
    text_lower = text.lower()

    flood_words = [
        "flood",
        "flooding",
        "बाढ़",
        "बाढ़",
    ]

    fire_words = [
        "fire",
        "आग",
    ]

    earthquake_words = [
        "earthquake",
        "भूकंप",
        "भूकम्प",
    ]

    medical_words = [
        "medical emergency",
        "medical",
        "ambulance",
        "hospital",
        "doctor",
        "patient",
        "injured",
        "injury",
        "एम्बुलेंस",
        "एम्बुलन्स",
        "अस्पताल",
        "डॉक्टर",
        "मरीज",
        "घायल",
        "चोट",
        "चिकित्सा आपातकाल",
    ]

    help_words = [
        "help",
        "help me",
        "i need help",
        "please help",
        "मदद",
        "मुझे मदद चाहिए",
        "बचाओ",
    ]

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

    if any(word in text_lower for word in flood_words):
        return "FLOOD_WARNING"

    if any(word in text_lower for word in fire_words):
        return "FIRE_WARNING"

    if any(word in text_lower for word in earthquake_words):
        return "EARTHQUAKE_WARNING"

    if any(word in text_lower for word in medical_words):
        return "MEDICAL_EMERGENCY"

    if any(word in text_lower for word in help_words):
        return "HELP_REQUEST"

    if any(word in text_lower for word in alert_words):
        return "ALERT"

    if any(word in text_lower for word in supply_words):
        return "SUPPLY_REQUEST"

    return "GENERAL_MESSAGE"


def encode_message(text):
    text = text.strip()

    language = detect_language(text)
    location = extract_location(text)
    object_name = extract_object(text)
    priority = extract_priority(text)
    intent = extract_intent(text)

    # Always preserve the original message.
    #
    # This is important because the semantic encoder may encounter
    # an object or phrase that is not present in our known vocabulary.
    # Instead of losing that information, the original message is
    # transmitted as a fallback.
    message = text

    return SemanticPacket(
        version=1,
        language=language,
        intent=intent,
        object=object_name,
        location=location,
        priority=priority,
        message=message,
    )

