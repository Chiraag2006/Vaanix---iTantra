import numpy as np


SAMPLES_PER_SYMBOL = 100
DEFAULT_SNR_DB = 5


def bpsk_modulate(bits, snr_db=DEFAULT_SNR_DB):
    """
    BPSK modulation with AWGN.

    snr_db represents Eb/N0 at the
    symbol decision point.
    """

    bits = np.asarray(bits, dtype=int)

    symbols = 2 * bits - 1

    t = (
        np.arange(SAMPLES_PER_SYMBOL)
        / SAMPLES_PER_SYMBOL
    )

    carrier = np.cos(
        2 * np.pi * t
    )

    pulse_train = np.repeat(
        symbols,
        SAMPLES_PER_SYMBOL
    )

    carrier_signal = np.tile(
        carrier,
        len(bits)
    )

    tx_signal = (
        pulse_train *
        carrier_signal
    )

    # --------------------------------------------------
    # AWGN
    # --------------------------------------------------
    #
    # The receiver performs correlation over
    # SAMPLES_PER_SYMBOL samples.
    #
    # Therefore the noise variance must account
    # for the integration/processing gain.
    #

    snr_linear = 10 ** (
        snr_db / 10
    )

    noise_variance = (
        SAMPLES_PER_SYMBOL
        / (2 * snr_linear)
    )

    noise = np.random.normal(
        0,
        np.sqrt(noise_variance),
        len(tx_signal)
    )

    rx_signal = (
        tx_signal +
        noise
    )

    return rx_signal, carrier


def bpsk_demodulate(
    rx_signal,
    carrier,
    num_bits
):
    """
    Coherent BPSK demodulation.
    """

    rx_symbols = np.zeros(
        num_bits
    )

    for i in range(num_bits):

        start = (
            i *
            SAMPLES_PER_SYMBOL
        )

        end = (
            start +
            SAMPLES_PER_SYMBOL
        )

        rx_symbols[i] = np.sum(
            rx_signal[start:end] *
            carrier
        )

    return (
        rx_symbols > 0
    ).astype(int)


def communication_channel(
    bits,
    snr_db=DEFAULT_SNR_DB
):
    """
    Complete BPSK + AWGN channel.
    """

    bits = np.asarray(
        bits,
        dtype=int
    )

    rx_signal, carrier = (
        bpsk_modulate(
            bits,
            snr_db
        )
    )

    rx_bits = bpsk_demodulate(
        rx_signal,
        carrier,
        len(bits)
    )

    return rx_bits


def calculate_ber(
    transmitted_bits,
    received_bits
):
    """
    Calculate Bit Error Rate.
    """

    transmitted_bits = np.asarray(
        transmitted_bits,
        dtype=int
    )

    received_bits = np.asarray(
        received_bits,
        dtype=int
    )

    if len(transmitted_bits) == 0:
        return 0.0

    errors = np.sum(
        transmitted_bits != received_bits
    )

    return (
        errors /
        len(transmitted_bits)
    )


if __name__ == "__main__":

    np.random.seed(42)

    test_bits = np.random.randint(
        0,
        2,
        10000
    )

    print("=" * 55)
    print("BPSK AWGN BER TEST")
    print("=" * 55)

    for snr in [
        0,
        2,
        5,
        8,
        10
    ]:

        received = (
            communication_channel(
                test_bits,
                snr
            )
        )

        ber = calculate_ber(
            test_bits,
            received
        )

        print(
            f"SNR = {snr:2d} dB | "
            f"BER = {ber:.4f}"
        )