import json


def json_to_bytes(data):
    """
    Convert semantic JSON data into UTF-8 bytes.
    UTF = Unicode Transformation Format – 8-bit
    """
    json_string = json.dumps(data, separators=(",", ":"))
    return json_string.encode("utf-8")


def bytes_to_json(data):
    """
    Convert UTF-8 bytes back into JSON.
    """
    json_string = data.decode("utf-8")
    return json.loads(json_string)


if __name__ == "__main__":

    semantic_data = {
        "text": "flood warning move to higher ground immediately",
        "lang": "en",
        "script": "Latin",
        "intent": "ALERT",
        "urgency": "HIGH"
    }

    encoded = json_to_bytes(semantic_data)

    print("Original JSON:")
    print(semantic_data)

    print("\nEncoded bytes:")
    print(encoded)

    print("\nNumber of bytes:")
    print(len(encoded))

    decoded = bytes_to_json(encoded)

    print("\nDecoded JSON:")
    print(decoded)