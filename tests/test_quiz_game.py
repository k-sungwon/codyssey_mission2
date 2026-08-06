import unittest

from quiz_game import QuizGame


class QuizGameInputTest(unittest.TestCase):
    def test_parse_number_accepts_valid_number(self):
        result = QuizGame.parse_number(" 2 ", 1, 5)

        self.assertEqual(result, 2)

    def test_parse_number_accepts_home(self):
        result = QuizGame.parse_number("home", 1, 5)

        self.assertEqual(result, "home")

    def test_parse_number_rejects_empty_input(self):
        result = QuizGame.parse_number("", 1, 5)

        self.assertIsNone(result)

    def test_parse_number_rejects_non_number(self):
        result = QuizGame.parse_number("abc", 1, 5)

        self.assertIsNone(result)

    def test_parse_number_rejects_out_of_range_number(self):
        result = QuizGame.parse_number("9", 1, 5)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
