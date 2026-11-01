"""
CipherVault – Vigenère Cipher Implementation
Keyword-based polyalphabetic substitution cipher.
Preserves non-alphabetic characters.
"""


def _validate_keyword(keyword: str) -> str:
    """Ensure the keyword contains only alphabetic characters."""
    if not keyword:
        raise ValueError("Keyword must not be empty.")
    if not keyword.isalpha():
        raise ValueError("Keyword must contain only alphabetic characters (A-Z).")
    return keyword.upper()


def vigenere_encrypt(plaintext: str, keyword: str) -> str:
    """Encrypt plaintext using the Vigenère cipher with the given keyword."""
    keyword = _validate_keyword(keyword)
    result = []
    key_index = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, keyword: str) -> str:
    """Decrypt ciphertext using the Vigenère cipher with the given keyword."""
    keyword = _validate_keyword(keyword)
    result = []
    key_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return ''.join(result)
