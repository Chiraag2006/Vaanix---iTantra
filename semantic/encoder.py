import re

from semantic.packet_schema import SemanticPacket


def extract_location(text):
    """
    Extract a sector number from the message.

    Examples:
        sector 4
        sector four
        sector 7
        sector seven
    """

    number_words = {
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

    match = re.search(
        r"sector\s+(\d+)",
        text.lower()
    )

    if match:
        return f"SECTOR_{match.group(1)}"

    for word, number in number_words.items():

        if re.search(
            rf"sector\s+{word}",
            text.lower()
        ):
            return f"SECTOR_{number}"

    return "UNKNOWN"


def extract_object(text):
    """
    Detect the main supply object.
    """

    text = text.lower()

    objects = [
        ("MEDICINE", ["medicine", "medicines", "medical supplies"]),
        ("WATER", ["water", "water supplies"]),
        ("FOOD", ["food", "food supplies"]),
        ("FUEL", ["fuel"]),
        ("BLOOD", ["blood"]),
        ("EQUIPMENT", ["equipment"]),
    ]

    for object_name, keywords in objects:

        for keyword in keywords:

            if keyword in text:
                return object_name

    return "UNKNOWN"


def extract_priority(text):
    """
    Determine message priority.
    """

    text = text.lower()

    high_priority_words = [
        "urgent",
        "urgently",
        "immediately",
        "emergency",
        "critical",
        "asap",
    ]

    for word in high_priority_words:

        if word in text:
            return "HIGH"

    return "NORMAL"


def encode_message(text):
    """
    Convert a natural-language message into a
    prototype semantic packet.

    This is a rule-based semantic encoder for the
    current prototype. It will later be replaceable
    with an NLP/LLM/intent model.
    """

    text = text.strip()

    location = extract_location(text)
    object_name = extract_object(text)
    priority = extract_priority(text)

    if any(
        phrase in text.lower()
        for phrase in [
            "send",
            "deliver",
            "supply",
            "supplies",
            "provide",
        ]
    ):
        intent = "SUPPLY_REQUEST"

    elif any(
        phrase in text.lower()
        for phrase in [
            "alert",
            "warning",
            "danger",
            "emergency",
        ]
    ):
        intent = "ALERT"

    else:
        intent = "GENERAL_MESSAGE"

    return SemanticPacket(
        version=1,
        language="en",
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
    ]

    for message in examples:

        packet = encode_message(message)

        print("\nMessage:")
        print(message)

        print("Semantic packet:")
        print(packet)