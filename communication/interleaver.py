def interleave(packets):
    """
    Simple packet interleaving simulation.

    The packets are reordered before transmission
    to simulate spreading consecutive data across
    different transmission positions.
    """

    if not packets:
        return []

    # Simple reverse-order interleaving
    return list(reversed(packets))


def deinterleave(packets):
    """
    Restore the original packet ordering.
    """

    if not packets:
        return []

    return list(reversed(packets))