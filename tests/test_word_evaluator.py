import unittest

from utils.word_evaluator import (
    evaluate_guess,
    CORRECT,
    PRESENT,
    ABSENT,
)


class TestWordEvaluator(unittest.TestCase):

    def test_all_correct(self):
        result = evaluate_guess("APPLE", "APPLE")

        self.assertEqual(
            result,
            [CORRECT, CORRECT, CORRECT, CORRECT, CORRECT],
        )

    def test_all_absent(self):
        result = evaluate_guess("APPLE", "MUSIC")

        self.assertEqual(
            result,
            [ABSENT, ABSENT, ABSENT, ABSENT, ABSENT],
        )

    def test_present_letter(self):
        result = evaluate_guess("APPLE", "PLEAD")

        self.assertIn(PRESENT, result)

    def test_mixed_result(self):
        result = evaluate_guess("APPLE", "ALERT")

        self.assertEqual(len(result), 5)

        self.assertIn(CORRECT, result)
        self.assertIn(PRESENT, result)

    def test_invalid_target_length(self):
        with self.assertRaises(ValueError):
            evaluate_guess("APP", "APPLE")

    def test_invalid_guess_length(self):
        with self.assertRaises(ValueError):
            evaluate_guess("APPLE", "APP")
    def test_duplicate_letter_handling(self):
        result = evaluate_guess("APPLE", "ALLEY")

        self.assertEqual(len(result), 5)

        self.assertEqual(result[0], CORRECT)
        self.assertEqual(result[1], PRESENT)

if __name__ == "__main__":
    unittest.main()