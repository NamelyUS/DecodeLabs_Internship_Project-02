"""Tests for input validation utilities."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from utils.validators import (
    validate_caesar_shift,
    validate_vigenere_keyword,
    validate_text_input,
)


class TestCaesarShiftValidation(unittest.TestCase):

    def test_valid_integer(self):
        self.assertEqual(validate_caesar_shift("5"), 5)

    def test_negative_integer(self):
        self.assertEqual(validate_caesar_shift("-3"), -3)

    def test_zero(self):
        self.assertEqual(validate_caesar_shift("0"), 0)

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            validate_caesar_shift("")

    def test_none(self):
        with self.assertRaises(ValueError):
            validate_caesar_shift(None)

    def test_non_numeric(self):
        with self.assertRaises(ValueError):
            validate_caesar_shift("abc")

    def test_float_string(self):
        with self.assertRaises(ValueError):
            validate_caesar_shift("3.5")


class TestVigenereKeywordValidation(unittest.TestCase):

    def test_valid_keyword(self):
        self.assertEqual(validate_vigenere_keyword("SECRET"), "SECRET")

    def test_empty(self):
        with self.assertRaises(ValueError):
            validate_vigenere_keyword("")

    def test_spaces_only(self):
        with self.assertRaises(ValueError):
            validate_vigenere_keyword("   ")

    def test_digits(self):
        with self.assertRaises(ValueError):
            validate_vigenere_keyword("KEY123")


class TestTextInputValidation(unittest.TestCase):

    def test_valid_text(self):
        self.assertEqual(validate_text_input("Hello"), "Hello")

    def test_empty(self):
        with self.assertRaises(ValueError):
            validate_text_input("")

    def test_none(self):
        with self.assertRaises(ValueError):
            validate_text_input(None)

    def test_whitespace_only(self):
        with self.assertRaises(ValueError):
            validate_text_input("   ")


if __name__ == "__main__":
    unittest.main()
