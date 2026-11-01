"""Tests for Vigenère Cipher."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from algorithms.vigenere import vigenere_encrypt, vigenere_decrypt


class TestVigenereEncrypt(unittest.TestCase):

    def test_basic_encrypt(self):
        self.assertEqual(vigenere_encrypt("HELLO", "KEY"), "RIJVS")

    def test_lowercase(self):
        self.assertEqual(vigenere_encrypt("hello", "key"), "rijvs")

    def test_mixed_case(self):
        result = vigenere_encrypt("Hello World", "KEY")
        self.assertEqual(result, "Rijvs Uyvjn")

    def test_preserve_punctuation(self):
        result = vigenere_encrypt("Hello, World!", "KEY")
        self.assertEqual(result, "Rijvs, Uyvjn!")

    def test_preserve_spaces_digits(self):
        # Manual: T(A)=T, e(B)=f, s(C)=u, t(A)=t → "Tfut 123"
        result = vigenere_encrypt("Test 123", "ABC")
        self.assertEqual(result, "Tfut 123")


class TestVigenereDecrypt(unittest.TestCase):

    def test_basic_decrypt(self):
        self.assertEqual(vigenere_decrypt("RIJVS", "KEY"), "HELLO")

    def test_roundtrip(self):
        original = "The Quick Brown Fox Jumps Over The Lazy Dog! 42"
        for keyword in ["KEY", "SECRET", "A", "LONGKEYWORD"]:
            encrypted = vigenere_encrypt(original, keyword)
            decrypted = vigenere_decrypt(encrypted, keyword)
            self.assertEqual(decrypted, original, f"Roundtrip failed for keyword='{keyword}'")


class TestVigenereValidation(unittest.TestCase):

    def test_empty_keyword(self):
        with self.assertRaises(ValueError):
            vigenere_encrypt("HELLO", "")

    def test_numeric_keyword(self):
        with self.assertRaises(ValueError):
            vigenere_encrypt("HELLO", "KEY123")

    def test_keyword_with_spaces(self):
        with self.assertRaises(ValueError):
            vigenere_encrypt("HELLO", "KEY WORD")


if __name__ == "__main__":
    unittest.main()
