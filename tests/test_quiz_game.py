import unittest
import tempfile
import os

from quiz import Quiz
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

    def test_parse_delete_command_accepts_valid_command(self):
        result = QuizGame.parse_delete_command(" d3 ", 5)

        self.assertEqual(result, 3)

    def test_parse_delete_command_rejects_out_of_range_command(self):
        result = QuizGame.parse_delete_command("d9", 5)

        self.assertIsNone(result)

    def test_parse_delete_command_rejects_plain_number(self):
        result = QuizGame.parse_delete_command("3", 5)

        self.assertIsNone(result)

    def test_question_score_applies_hint_penalty_only_when_correct(self):
        quiz = Quiz("Python 기초", "리스트?", ["()", "[]", "{}", "<>"], 2, "대괄호", 100, 30)

        self.assertEqual(QuizGame.calculate_question_score(quiz, used_hint=False, correct=True), 100)
        self.assertEqual(QuizGame.calculate_question_score(quiz, used_hint=True, correct=True), 70)
        self.assertEqual(QuizGame.calculate_question_score(quiz, used_hint=True, correct=False), 0)

    def test_record_score_updates_history_and_best_score(self):
        path = os.path.join(tempfile.mkdtemp(prefix="quiz-game-score-"), "state.json")
        game = QuizGame("tester", path)

        game.record_score(70, 100, 1, 1, 1)

        self.assertEqual(game.best_score, 70)
        self.assertEqual(len(game.score_history), 1)
        self.assertEqual(game.score_history[0]["nickname"], "tester")
        self.assertEqual(game.score_history[0]["used_hint_count"], 1)


if __name__ == "__main__":
    unittest.main()
