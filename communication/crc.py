import zlib


def generate_crc(packet):
    """
    Generate a CRC checksum for a semantic packet.

    The packet is converted into a deterministic string
    before calculating the checksum.
    """

    packet_string = (
        f"{packet.version}|"
        f"{packet.language}|"
        f"{packet.intent}|"
        f"{packet.object}|"
        f"{packet.location}|"
        f"{packet.priority}"
    )

    return zlib.crc32(
        packet_string.encode("utf-8")
    )


def verify_crc(packet, expected_crc):
    """
    Verify whether the packet matches the expected CRC.
    """

    actual_crc = generate_crc(packet)

    return actual_crc == expected_crc