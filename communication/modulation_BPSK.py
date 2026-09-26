import numpy as np

# ---------------------------------------------------------
# 1. Input Bit Sequence
# ---------------------------------------------------------
bits = np.random.randint(0, 2, 10000)
num_bits = len(bits)

# ---------------------------------------------------------
# 2. BPSK Mapping (1 -> +1, 0 -> -1)
# ---------------------------------------------------------
# b_n = 2*bit - 1 maps 0 to -1 and 1 to +1
symbols = 2 * bits - 1

# ---------------------------------------------------------
# 3. Carrier Waveform Generation
# ---------------------------------------------------------
samples_per_symbol = 100
t_sym = np.linspace(0, 1, samples_per_symbol, endpoint=False)
carrier = np.cos(2 * np.pi * 1 * t_sym)  # 1 cycle per bit for illustration

# Generate baseband pulse train, then modulate by carrier
pulse_train = np.repeat(symbols, samples_per_symbol)
full_carrier = np.tile(carrier, num_bits)
tx_waveform = pulse_train * full_carrier

# ---------------------------------------------------------
# 4. Add Channel Noise (AWGN)-->(Additive White Gaussian Noise)
# ---------------------------------------------------------
noise_std = 8.0  # Adjust noise level
noise = np.random.normal(0, noise_std, len(tx_waveform))
rx_waveform = tx_waveform + noise

# ---------------------------------------------------------
# 5. BPSK Demodulator (Coherent Detection)
# ---------------------------------------------------------
# Correlate with carrier over each symbol interval (matched filter)
rx_symbols = np.zeros(num_bits)
for i in range(num_bits):
    start = i * samples_per_symbol
    end = (i + 1) * samples_per_symbol
    # Multiply by the known carrier and integrate (sum)
    rx_symbols[i] = np.sum(rx_waveform[start:end] * carrier)

# Hard decision threshold at 0: r > 0 -> 1, r <= 0 -> 0
rx_bits = (rx_symbols > 0).astype(int)

# ---------------------------------------------------------
# 6. BER Calculation
# ---------------------------------------------------------
errors = np.sum(bits != rx_bits)
ber = errors / num_bits

print(f"Original Bits : {bits.tolist()}")
print(f"Received Bits : {rx_bits.tolist()}")
print(f"Bit Errors    : {errors} / {num_bits}")
print(f"Measured BER  : {ber:.4f}")