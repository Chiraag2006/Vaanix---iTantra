import random

from communication.crc import (
    generate_crc,
    verify_crc
)

from communication.fec import (
    add_redundancy,
    recover_packet
)

from communication.interleaver import (
    interleave,
    deinterleave
)


def transmit_single(
    packet,
    packet_loss=0.0,
    corruption_probability=0.0
):
    """
    Simulate transmission of one packet.

    Returns:
        (packet, crc_valid)
    """

    # ----------------------------------------------
    # PACKET LOSS
    # ----------------------------------------------

    if random.random() < packet_loss:
        return None, False


    # ----------------------------------------------
    # GENERATE CRC
    # ----------------------------------------------

    original_crc = generate_crc(packet)


    # ----------------------------------------------
    # SIMULATE CORRUPTION
    # ----------------------------------------------

    if random.random() < corruption_probability:

        packet.priority = "CORRUPTED"


    # ----------------------------------------------
    # CRC VERIFICATION
    # ----------------------------------------------

    crc_valid = verify_crc(
        packet,
        original_crc
    )


    # ----------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------

    if not crc_valid:
        return packet, False

    return packet, True


def transmit(
    packet,
    packet_loss=0.0,
    corruption_probability=0.0
):
    """
    Full prototype communication pipeline.

    Pipeline:

        Semantic Packet
              ↓
             FEC
              ↓
         Interleaving
              ↓
           Channel
              ↓
        Deinterleaving
              ↓
         FEC Recovery
    """

    # ----------------------------------------------
    # FEC ENCODING
    # ----------------------------------------------

    redundant_packets = add_redundancy(
        packet,
        copies=3
    )


    # ----------------------------------------------
    # INTERLEAVING
    # ----------------------------------------------

    interleaved_packets = interleave(
        redundant_packets
    )


    # ----------------------------------------------
    # TRANSMISSION
    # ----------------------------------------------

    received_packets = []

    for current_packet in interleaved_packets:

        received_packet, crc_valid = (
            transmit_single(
                current_packet,
                packet_loss,
                corruption_probability
            )
        )

        received_packets.append(
            (
                received_packet,
                crc_valid
            )
        )


    # ----------------------------------------------
    # DEINTERLEAVING
    # ----------------------------------------------

    deinterleaved_packets = deinterleave(
        received_packets
    )


    # ----------------------------------------------
    # FEC RECOVERY
    # ----------------------------------------------

    recovered_packet = recover_packet(
        deinterleaved_packets
    )


    # ----------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------

    if recovered_packet is None:

        return None, False, False

    return recovered_packet, True, True