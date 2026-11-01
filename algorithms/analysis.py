"""
CipherVault – Text Analysis Utilities
Character frequency analysis for ciphertext inspection.
"""

from collections import Counter


def character_frequency(text: str) -> dict:
    """
    Return a dict with:
      total_chars, alpha_chars, unique_chars,
      frequency (dict of char → count, alphabetic only, case-insensitive).
    """
    alpha_only = [ch.lower() for ch in text if ch.isalpha()]
    freq = dict(Counter(alpha_only).most_common())
    return {
        "total_chars": len(text),
        "alpha_chars": len(alpha_only),
        "unique_chars": len(set(alpha_only)),
        "frequency": freq,
    }
