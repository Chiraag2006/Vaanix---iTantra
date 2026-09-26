from Packetiser import json_to_bytes, bytes_to_json
from CRC import add_crc, verify_crc
from FEC import (
    hamming_encode_message,
    hamming_decode_message,
    bits_to_bytes
)
from Interleaver import interleave, deinterleave
from Channel import flip_bit, burst_error


# =====================================================
# SENDER
# =====================================================

semantic_data = {
    "text": "flood warning move to higher ground immediately",
    "lang": "en",
    "script": "Latin",
    "intent": "ALERT",
    "urgency": "HIGH"
}

print("=" * 70)
print("iTANTRA SEMANTIC VOICE RELAY")
print("END-TO-END TRANSMISSION TEST")
print("=" * 70)


print("\n[SENDER]")
print("-" * 70)

print("Original JSON:")
print(semantic_data)


# =====================================================
# 1. JSON → UTF-8 BYTES
# =====================================================

data = json_to_bytes(semantic_data)

print("\nJSON → UTF-8 bytes:")
print(data)

print("Payload size:", len(data), "bytes")


# =====================================================
# 2. CRC
# =====================================================

packet = add_crc(data)

print("\nCRC added.")
print("Packet size:", len(packet), "bytes")


# =====================================================
# 3. FEC
# =====================================================

encoded = hamming_encode_message(packet)

print("\nFEC encoded.")
print("FEC bit count:", len(encoded))


# =====================================================
# 4. INTERLEAVING
# =====================================================

interleaved = interleave(encoded, 7)

print("\nInterleaving complete.")
print("Transmitted bit count:", len(interleaved))


# =====================================================
# CHANNEL
# =====================================================

print("\n[CHANNEL]")
print("-" * 70)

# -----------------------------------------------------
# Choose ONE test
# -----------------------------------------------------

# TEST 1 — No error
# received = interleaved.copy()

# TEST 2 — One bit error
# received = flip_bit(interleaved, 10)

# TEST 3 — Three-bit burst error
received = burst_error(interleaved, 10, 3)


print("Channel simulation complete.")

print("Original transmitted bits:", len(interleaved))
print("Received bits:", len(received))


# =====================================================
# RECEIVER
# =====================================================

print("\n[RECEIVER]")
print("-" * 70)


# =====================================================
# 5. DEINTERLEAVING
# =====================================================

deinterleaved = deinterleave(received, 7)

print("Deinterleaving complete.")


# =====================================================
# 6. FEC DECODING
# =====================================================

decoded_bits = hamming_decode_message(deinterleaved)

print("FEC decoding complete.")


# =====================================================
# 7. BITS → BYTES
# =====================================================

decoded_packet = bits_to_bytes(decoded_bits)

print("Recovered packet bytes:", len(decoded_packet))


# =====================================================
# 8. CRC CHECK
# =====================================================

valid, recovered_payload, received_crc, calculated_crc = verify_crc(
    decoded_packet
)

print("\nCRC CHECK")
print("Received CRC:  ", received_crc)
print("Calculated CRC:", calculated_crc)

if valid:
    print("CRC STATUS: ✅ VALID")
else:
    print("CRC STATUS: ❌ INVALID")


# =====================================================
# 9. CRC RESULT
# =====================================================

if not valid:

    print("\n❌ PACKET REJECTED")
    print("The received data is corrupted.")

else:

    # =================================================
    # 10. BYTES → JSON
    # =================================================

    recovered_json = bytes_to_json(recovered_payload)

    print("\nRecovered JSON:")
    print(recovered_json)


    # =================================================
    # FINAL COMPARISON
    # =================================================

    print("\n" + "=" * 70)

    if recovered_json == semantic_data:

        print("✅ SUCCESS")
        print("Original JSON recovered exactly.")

    else:

        print("❌ FAILURE")
        print("Recovered JSON does not match original.")

    print("=" * 70)