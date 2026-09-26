from copy import deepcopy


def add_redundancy(packet, copies=3):
    """
    Create redundant copies of a semantic packet.

    This is a simple prototype FEC/repetition scheme.
    The same packet is transmitted multiple times so that
    the receiver can recover the message if some copies
    are lost or corrupted.
    """

    return [
        deepcopy(packet)
        for _ in range(copies)
    ]


def recover_packet(received_packets):
    """
    Recover a packet from received redundant copies.

    Returns the first valid packet available.
    Returns None if no packet was successfully received.
    """

    for packet, crc_valid in received_packets:

        if packet is not None and crc_valid:
            return packet

    return None