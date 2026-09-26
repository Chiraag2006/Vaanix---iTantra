def hamming_encode(data_bits):
    """
    Encode 4 data bits using Hamming(7,4).

    Input:
        [d1, d2, d3, d4]

    Output:
        [p1, p2, d1, p3, d2, d3, d4]
    """

    d1, d2, d3, d4 = data_bits

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    return [p1, p2, d1, p3, d2, d3, d4]


def hamming_decode(bits):
    """
    Decode a Hamming(7,4) codeword
    and correct one-bit error.
    """

    # Positions:
    # 1  2  3  4  5  6  7
    # p1 p2 d1 p3 d2 d3 d4

    p1, p2, d1, p3, d2, d3, d4 = bits

    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s3 = p3 ^ d2 ^ d3 ^ d4

    error_position = s1 + (s2 * 2) + (s3 * 4)

    if error_position != 0:
        print("Error detected at position:", error_position)

        bits[error_position - 1] ^= 1

    else:
        print("No error detected")

    return [bits[2], bits[4], bits[5], bits[6]]


def byte_to_bits(byte):
    return [(byte >> i) & 1 for i in range(7, -1, -1)]


def bytes_to_bits(data):
    bits = []

    for byte in data:
        bits.extend(byte_to_bits(byte))

    return bits


def hamming_encode_message(data):
    """
    Convert bytes into bits and apply Hamming(7,4)
    to every 4 bits.
    """

    bits = bytes_to_bits(data)

    encoded = []

    for i in range(0, len(bits), 4):

        chunk = bits[i:i+4]

        # Add zeros if necessary
        while len(chunk) < 4:
            chunk.append(0)

        encoded.extend(hamming_encode(chunk))

    return encoded


def hamming_decode_message(encoded_bits):
    """
    Decode the complete Hamming encoded bitstream.
    """

    decoded = []

    for i in range(0, len(encoded_bits), 7):

        chunk = encoded_bits[i:i+7]

        data = hamming_decode(chunk)

        decoded.extend(data)

    return decoded


def bits_to_bytes(bits):
    """
    Convert a list of bits back into bytes.
    """

    data = []

    for i in range(0, len(bits), 8):

        byte_bits = bits[i:i+8]

        value = 0

        for bit in byte_bits:
            value = (value << 1) | bit

        data.append(value)

    return bytes(data)


# ------------------------------------------------
# TEST CODE
# ------------------------------------------------

if __name__ == "__main__":

    data = b"Hi"

    print("Original bytes:", data)

    # Bytes → bits
    bits = bytes_to_bits(data)

    print("Original bits:", bits)

    # FEC encode
    encoded = hamming_encode_message(data)

    print("FEC encoded bits:", encoded)

    print("Original bit count:", len(bits))
    print("FEC bit count:", len(encoded))

    # Introduce one error
    received = encoded.copy()

    received[10] ^= 1

    print("Received with error:", received)

    # FEC decode
    decoded_bits = hamming_decode_message(received)

    print("Decoded bits:", decoded_bits)

    # Bits → bytes
    decoded_bytes = bits_to_bytes(decoded_bits)

    print("Recovered bytes:", decoded_bytes)

    # Bytes → text
    print("Recovered message:", decoded_bytes.decode("utf-8"))