"""
CipherVault – Caesar Cipher Implementation
Supports encryption and decryption with arbitrary integer shift values.
Preserves non-alphabetic characters (spaces, digits, punctuation).
"""


def caesar_encrypt(plaintext: str, shift: int) -> str:
    """Encrypt plaintext using the Caesar cipher with the given shift."""
    shift = shift % 26  # Normalize shift to 0-25
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt ciphertext by reversing the Caesar shift."""
    return caesar_encrypt(ciphertext, -shift)


def caesar_brute_force(ciphertext: str) -> list[dict]:
    """
    Try all 25 non-zero shifts and return a list of
    {"shift": int, "text": str} dicts.
    """
    results = []
    for shift in range(1, 26):
        results.append({
            "shift": shift,
            "text": caesar_decrypt(ciphertext, shift),
        })
    return results
