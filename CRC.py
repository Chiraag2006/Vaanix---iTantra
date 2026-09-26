import zlib


CRC_SIZE = 4


def calculate_crc(data):
    """
    Calculate CRC-32 for the given bytes.
    """
    return zlib.crc32(data) & 0xFFFFFFFF


def add_crc(data):
    """
    Append the 4-byte CRC-32 to the payload.

    Example:

        payload + CRC
    """

    crc = calculate_crc(data)

    crc_bytes = crc.to_bytes(4, "big")

    return data + crc_bytes


def verify_crc(packet):
    """
    Separate the payload and CRC.

    Returns:

        valid
        payload
        received_crc
        calculated_crc
    """

    if len(packet) < CRC_SIZE:
        return False, b"", None, None

    # Last 4 bytes = CRC
    payload = packet[:-CRC_SIZE]

    # Convert received CRC bytes → integer
    received_crc = int.from_bytes(
        packet[-CRC_SIZE:],
        "big"
    )

    # Calculate CRC again
    calculated_crc = calculate_crc(payload)

    valid = received_crc == calculated_crc

    return (
        valid,
        payload,
        received_crc,
        calculated_crc
    )


# =====================================================
# TEST CRC
# =====================================================

if __name__ == "__main__":

    data = b"flood warning"

    print("Original data:")
    print(data)

    # Sender adds CRC
    packet = add_crc(data)

    print("\nPacket with CRC:")
    print(packet)

    # Receiver checks CRC
    valid, payload, received_crc, calculated_crc = verify_crc(packet)

    print("\nReceived CRC:")
    print(received_crc)

    print("Calculated CRC:")
    print(calculated_crc)

    print("CRC valid:", valid)