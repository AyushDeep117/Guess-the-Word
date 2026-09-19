import unittest

from utils.validators import (
    validate_username,
    validate_password,
    validate_guess,
)


class TestValidators(unittest.TestCase):

    def test_valid_username(self):
        valid, message = validate_username("Ayush")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_username_too_short(self):
        valid, message = validate_username("Ayu")
        self.assertFalse(valid)

    def test_username_with_numbers(self):
        valid, message = validate_username("Ayush123")
        self.assertFalse(valid)

    def test_valid_password(self):
        valid, message = validate_password("abc12$")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_password_too_short(self):
        valid, message = validate_password("a1$")
        self.assertFalse(valid)

    def test_password_without_number(self):
        valid, message = validate_password("abcde$")
        self.assertFalse(valid)

    def test_password_without_special_character(self):
        valid, message = validate_password("abc123")
        self.assertFalse(valid)

    def test_valid_guess(self):
        valid, message = validate_guess("APPLE")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_guess_wrong_length(self):
        valid, message = validate_guess("APP")
        self.assertFalse(valid)

    def test_guess_with_numbers(self):
        valid, message = validate_guess("APP12")
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()