def interleave(bits, codeword_size=7):
    """
    Arrange FEC codewords as rows and transmit column-wise.

    For Hamming(7,4), each row contains 7 bits.
    """

    if len(bits) % codeword_size != 0:
        raise ValueError(
            "FEC bits must be divisible by codeword_size."
        )

    rows = len(bits) // codeword_size

    # Create matrix
    matrix = []

    for i in range(rows):
        row = bits[i * codeword_size:(i + 1) * codeword_size]
        matrix.append(row)

    # Read column by column
    result = []

    for col in range(codeword_size):
        for row in range(rows):
            result.append(matrix[row][col])

    return result


def deinterleave(bits, codeword_size=7):
    """
    Reverse the interleaving operation.
    """

    if len(bits) % codeword_size != 0:
        raise ValueError(
            "Interleaved bits must be divisible by codeword_size."
        )

    rows = len(bits) // codeword_size

    # Empty matrix
    matrix = []

    for _ in range(rows):
        matrix.append([0] * codeword_size)

    index = 0

    # Put transmitted bits back column by column
    for col in range(codeword_size):
        for row in range(rows):
            matrix[row][col] = bits[index]
            index += 1

    # Read rows back
    result = []

    for row in range(rows):
        for col in range(codeword_size):
            result.append(matrix[row][col])

    return result


# Test this file directly
if __name__ == "__main__":

    bits = [
        1, 0, 1, 1, 0, 0, 1,
        0, 1, 1, 0, 1, 0, 1,
        1, 1, 0, 0, 0, 1, 0
    ]

    print("Original:    ", bits)

    interleaved = interleave(bits)

    print("Interleaved: ", interleaved)

    recovered = deinterleave(interleaved)

    print("Recovered:   ", recovered)

    print("Test passed:", bits == recovered)