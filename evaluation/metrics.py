import time


def measure_latency(function, *args, **kwargs):

    start = time.perf_counter()

    result = function(
        *args,
        **kwargs
    )

    end = time.perf_counter()

    latency_ms = (
        end - start
    ) * 1000

    return result, latency_ms


def estimate_packet_size(packet):

    """
    Estimate the size of the semantic packet
    using its current text representation.

    This is only a prototype estimate.
    The final system will use compact serialization.
    """

    packet_string = (
        f"{packet.version}|"
        f"{packet.language}|"
        f"{packet.intent}|"
        f"{packet.object}|"
        f"{packet.location}|"
        f"{packet.priority}"
    )

    return len(
        packet_string.encode("utf-8")
    )


def calculate_compression_ratio(
    original_bytes,
    semantic_bytes
):

    if semantic_bytes == 0:
        return 0

    return (
        original_bytes /
        semantic_bytes
    )


def semantic_fidelity(
    original_text,
    recovered_text
):

    """
    Basic prototype semantic fidelity check.

    Returns:
        1.0 = exact normalized match
        0.0 = mismatch
    """

    original = " ".join(
        original_text.lower().split()
    )

    recovered = " ".join(
        recovered_text.lower().split()
    )

    return (
        1.0
        if original == recovered
        else 0.0
    )