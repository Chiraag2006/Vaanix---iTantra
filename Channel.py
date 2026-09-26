import random


def flip_bit(bits, position):
    """
    Flip exactly one bit.

    position is zero-based:
    0 = first bit
    1 = second bit
    etc.
    """

    if position < 0 or position >= len(bits):
        raise IndexError("Bit position is outside the data.")

    received = bits.copy()

    # 0 becomes 1, 1 becomes 0
    received[position] ^= 1

    return received


def burst_error(bits, start, length):
    """
    Flip a consecutive group of bits.

    Example:
        start = 10
        length = 3

    flips:
        positions 10, 11, 12
    """

    if start < 0 or start + length > len(bits):
        raise IndexError("Burst is outside the data.")

    received = bits.copy()

    for i in range(start, start + length):
        received[i] ^= 1

    return received


def noisy_channel(bits, error_probability, seed=None):
    """
    Randomly flip bits according to error_probability.

    Example:
        0.01 = approximately 1% chance per bit
    """

    if error_probability < 0 or error_probability > 1:
        raise ValueError(
            "error_probability must be between 0 and 1."
        )

    rng = random.Random(seed)

    received = bits.copy()

    for i in range(len(received)):

        if rng.random() < error_probability:
            received[i] ^= 1

    return received


# =====================================================
# TEST CHANNEL
# =====================================================

if __name__ == "__main__":

    bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]

    print("Original:")
    print(bits)

    print("\nOne bit error:")
    print(flip_bit(bits, 3))

    print("\nBurst error:")
    print(burst_error(bits, 3, 3))

    print("\nRandom noisy channel:")
    print(noisy_channel(bits, 0.2))