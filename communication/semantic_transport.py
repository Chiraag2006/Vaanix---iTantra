from Packetiser import json_to_bytes, bytes_to_json
from CRC import add_crc, verify_crc
from FEC import (
    hamming_encode_message,
    hamming_decode_message,
    bits_to_bytes,
)
from Interleaver import interleave, deinterleave

from communication.modulation_BPSK import (
    communication_channel,
    calculate_ber,
)

from semantic.packet_schema import SemanticPacket


def packet_to_dict(packet: SemanticPacket):
    return {
        "version": packet.version,
        "language": packet.language,
        "intent": packet.intent,
        "object": packet.object,
        "location": packet.location,
        "priority": packet.priority,
        "message": packet.message,
    }


def dict_to_packet(data):
    return SemanticPacket(
        version=data["version"],
        language=data["language"],
        intent=data["intent"],
        object=data["object"],
        location=data["location"],
        priority=data["priority"],
        message=data.get("message", ""),
    )


def transmit_semantic_packet(packet: SemanticPacket, snr_db=5):
    semantic_data = packet_to_dict(packet)

    payload = json_to_bytes(semantic_data)

    packet_with_crc = add_crc(payload)

    encoded_bits = hamming_encode_message(packet_with_crc)

    interleaved_bits = interleave(encoded_bits, 7)

    received_bits = communication_channel(
        interleaved_bits,
        snr_db,
    )

    ber = calculate_ber(
        interleaved_bits,
        received_bits,
    )

    deinterleaved_bits = deinterleave(
        received_bits,
        7,
    )

    decoded_bits = hamming_decode_message(
        deinterleaved_bits
    )

    decoded_packet = bits_to_bytes(decoded_bits)

    valid, recovered_payload, received_crc, calculated_crc = (
        verify_crc(decoded_packet)
    )

    if not valid:
        return {
            "success": False,
            "packet": None,
            "crc_valid": False,
            "payload_size": len(payload),
            "packet_size": len(packet_with_crc),
            "fec_bits": len(encoded_bits),
            "tx_bits": len(interleaved_bits),
            "rx_bits": len(received_bits),
            "snr_db": snr_db,
            "ber": ber,
            "received_crc": received_crc,
            "calculated_crc": calculated_crc,
        }

    recovered_data = bytes_to_json(
        recovered_payload
    )

    recovered_packet = dict_to_packet(
        recovered_data
    )

    return {
        "success": True,
        "packet": recovered_packet,
        "crc_valid": True,
        "payload_size": len(payload),
        "packet_size": len(packet_with_crc),
        "fec_bits": len(encoded_bits),
        "tx_bits": len(interleaved_bits),
        "rx_bits": len(received_bits),
        "snr_db": snr_db,
        "ber": ber,
        "received_crc": received_crc,
        "calculated_crc": calculated_crc,
    }