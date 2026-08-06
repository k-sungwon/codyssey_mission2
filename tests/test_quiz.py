import unittest

from quiz import Quiz


class QuizTest(unittest.TestCase):
    def test_quiz_checks_correct_answer(self):
        quiz = Quiz("Python 기초", "리스트 기호는?", ["()", "[]", "{}", "<>"], 2, "대괄호")

        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))

    def test_quiz_converts_to_and_from_dict(self):
        quiz = Quiz("경제 상식", "수요가 늘면?", ["가격 상승", "항상 하락", "변화 없음", "폐지"], 1, "시장 가격", 100, 30)

        restored = Quiz.from_dict(quiz.to_dict())

        self.assertEqual(restored.category, "경제 상식")
        self.assertEqual(restored.choices[0], "가격 상승")
        self.assertEqual(restored.answer, 1)

    def test_quiz_requires_four_choices(self):
        with self.assertRaises(ValueError):
            Quiz("Python 기초", "문제", ["1", "2", "3"], 1, "힌트")

    def test_quiz_answer_must_be_between_one_and_four(self):
        with self.assertRaises(ValueError):
            Quiz("Python 기초", "문제", ["1", "2", "3", "4"], 5, "힌트")


if __name__ == "__main__":
    unittest.main()
