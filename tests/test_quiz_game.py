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

        self.assertEqual(result, [3])

    def test_parse_delete_command_rejects_out_of_range_command(self):
        result = QuizGame.parse_delete_command("d9", 5)

        self.assertIsNone(result)

    def test_parse_delete_command_rejects_plain_number(self):
        result = QuizGame.parse_delete_command("3", 5)

        self.assertIsNone(result)

    def test_parse_delete_command_accepts_multiple_numbers(self):
        result = QuizGame.parse_delete_command("d2 4 5", 5)

        self.assertEqual(result, [2, 4, 5])

    def test_parse_delete_command_rejects_duplicates(self):
        result = QuizGame.parse_delete_command("d2 2", 5)

        self.assertIsNone(result)

    def test_parse_detail_action_accepts_play_and_detail(self):
        self.assertEqual(QuizGame.parse_detail_action("1"), "play")
        self.assertEqual(QuizGame.parse_detail_action("2"), "detail")

    def test_parse_detail_action_accepts_home(self):
        self.assertEqual(QuizGame.parse_detail_action("home"), "home")

    def test_parse_detail_action_rejects_invalid_input(self):
        self.assertIsNone(QuizGame.parse_detail_action("9"))

    def test_parse_reset_command_accepts_reset(self):
        self.assertTrue(QuizGame.parse_reset_command(" reset "))
        self.assertFalse(QuizGame.parse_reset_command("1"))

    def test_get_sorted_score_history_sorts_by_highest_score(self):
        records = [
            {"nickname": "low", "score": 10, "played_at": "2026-08-06 10:00:00"},
            {"nickname": "high", "score": 90, "played_at": "2026-08-06 09:00:00"},
            {"nickname": "mid", "score": 50, "played_at": "2026-08-06 11:00:00"},
        ]

        sorted_records = QuizGame.get_sorted_score_history(records)

        self.assertEqual([record["nickname"] for record in sorted_records], ["high", "mid", "low"])

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
