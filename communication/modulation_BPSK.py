import numpy as np

SAMPLES_PER_SYMBOL = 100
SNR_DB = 5


def bpsk_modulate(bits):
    bits = np.asarray(bits, dtype=int)

    symbols = 2 * bits - 1

    t = np.arange(SAMPLES_PER_SYMBOL) / SAMPLES_PER_SYMBOL
    carrier = np.cos(2 * np.pi * t)

    pulse_train = np.repeat(symbols, SAMPLES_PER_SYMBOL)
    carrier_signal = np.tile(carrier, len(bits))

    tx_signal = pulse_train * carrier_signal

    signal_power = np.mean(tx_signal ** 2)
    snr_linear = 10 ** (SNR_DB / 10)
    noise_power = signal_power / snr_linear

    noise = np.random.normal(
        0,
        np.sqrt(noise_power),
        len(tx_signal)
    )

    rx_signal = tx_signal + noise

    return rx_signal, carrier


def bpsk_demodulate(rx_signal, carrier, num_bits):
    rx_symbols = np.zeros(num_bits)

    for i in range(num_bits):
        start = i * SAMPLES_PER_SYMBOL
        end = start + SAMPLES_PER_SYMBOL

        rx_symbols[i] = np.sum(
            rx_signal[start:end] * carrier
        )

    return (rx_symbols > 0).astype(int)


def communication_channel(bits):
    bits = np.asarray(bits, dtype=int)

    rx_signal, carrier = bpsk_modulate(bits)

    rx_bits = bpsk_demodulate(
        rx_signal,
        carrier,
        len(bits)
    )

    return rx_bits