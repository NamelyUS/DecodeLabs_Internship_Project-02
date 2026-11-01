"""Tests for Caesar Cipher."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from algorithms.caesar import caesar_encrypt, caesar_decrypt, caesar_brute_force


class TestCaesarEncrypt(unittest.TestCase):

    def test_shift_3(self):
        self.assertEqual(caesar_encrypt("HELLO", 3), "KHOOR")

    def test_shift_3_lowercase(self):
        self.assertEqual(caesar_encrypt("hello", 3), "khoor")

    def test_mixed_case(self):
        self.assertEqual(caesar_encrypt("Hello World", 3), "Khoor Zruog")

    def test_shift_0(self):
        self.assertEqual(caesar_encrypt("Hello", 0), "Hello")

    def test_shift_26(self):
        self.assertEqual(caesar_encrypt("Hello", 26), "Hello")

    def test_shift_greater_than_26(self):
        self.assertEqual(caesar_encrypt("ABC", 29), caesar_encrypt("ABC", 3))

    def test_negative_shift(self):
        self.assertEqual(caesar_encrypt("KHOOR", -3), "HELLO")

    def test_preserve_punctuation(self):
        self.assertEqual(caesar_encrypt("Hello, World! 123", 5), "Mjqqt, Btwqi! 123")

    def test_preserve_spaces(self):
        self.assertEqual(caesar_encrypt("A B C", 1), "B C D")

    def test_empty_string(self):
        self.assertEqual(caesar_encrypt("", 5), "")

    def test_all_punctuation(self):
        self.assertEqual(caesar_encrypt("!@#$%", 10), "!@#$%")


class TestCaesarDecrypt(unittest.TestCase):

    def test_decrypt_shift_3(self):
        self.assertEqual(caesar_decrypt("KHOOR", 3), "HELLO")

    def test_decrypt_lowercase(self):
        self.assertEqual(caesar_decrypt("khoor", 3), "hello")

    def test_roundtrip(self):
        original = "The Quick Brown Fox Jumps Over The Lazy Dog! 42"
        for shift in [-5, 0, 3, 13, 25, 26, 52, 100]:
            encrypted = caesar_encrypt(original, shift)
            decrypted = caesar_decrypt(encrypted, shift)
            self.assertEqual(decrypted, original, f"Roundtrip failed for shift={shift}")


class TestCaesarBruteForce(unittest.TestCase):

    def test_returns_25_results(self):
        results = caesar_brute_force("KHOOR")
        self.assertEqual(len(results), 25)

    def test_correct_shift_found(self):
        results = caesar_brute_force("KHOOR")
        texts = [r["text"] for r in results]
        self.assertIn("HELLO", texts)

    def test_shifts_are_1_to_25(self):
        results = caesar_brute_force("TEST")
        shifts = [r["shift"] for r in results]
        self.assertEqual(shifts, list(range(1, 26)))


if __name__ == "__main__":
    unittest.main()
