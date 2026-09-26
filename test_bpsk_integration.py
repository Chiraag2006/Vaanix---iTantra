from Packetiser import json_to_bytes, bytes_to_json
from CRC import add_crc, verify_crc
from FEC import hamming_encode_message, hamming_decode_message, bits_to_bytes
from Interleaver import interleave, deinterleave
from communication.modulation_BPSK import communication_channel


semantic_data = {
    "text": "flood warning move to higher ground immediately",
    "lang": "en",
    "script": "Latin",
    "intent": "ALERT",
    "urgency": "HIGH"
}

print("=" * 70)
print("iTANTRA BPSK INTEGRATION TEST")
print("=" * 70)

# -------------------------
# SENDER
# -------------------------

payload = json_to_bytes(semantic_data)
packet = add_crc(payload)

print("\n[SENDER]")
print("Payload bytes:", len(payload))
print("Packet bytes :", len(packet))

encoded_bits = hamming_encode_message(packet)
interleaved_bits = interleave(encoded_bits, 7)

print("FEC bits     :", len(encoded_bits))
print("TX bits      :", len(interleaved_bits))

# -------------------------
# BPSK CHANNEL
# -------------------------

print("\n[BPSK CHANNEL]")
print("-" * 70)

received_bits = communication_channel(interleaved_bits)

print("RX bits      :", len(received_bits))

# -------------------------
# RECEIVER
# -------------------------

deinterleaved_bits = deinterleave(received_bits, 7)

decoded_bits = hamming_decode_message(deinterleaved_bits)

decoded_packet = bits_to_bytes(decoded_bits)

valid, recovered_payload, received_crc, calculated_crc = verify_crc(
    decoded_packet
)

print("\n[RECEIVER]")
print("-" * 70)

print("CRC valid:", valid)

if valid:
    recovered_data = bytes_to_json(recovered_payload)

    print("\nRecovered JSON:")
    print(recovered_data)

    if recovered_data == semantic_data:
        print("\nSUCCESS: Original semantic data recovered exactly.")
    else:
        print("\nWARNING: Data recovered but does not exactly match.")

else:
    print("\nFAILURE: CRC validation failed.")

print("=" * 70)