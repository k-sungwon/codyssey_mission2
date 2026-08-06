import json
import tempfile
import unittest

from storage import load_state, save_state


class StorageTest(unittest.TestCase):
    def test_load_state_uses_defaults_when_file_missing(self):
        with self.subTest("missing file loads default quizzes"):
            path = self.tmp_path("missing-state.json")
            state = load_state(path)

            self.assertEqual(len(state["quizzes"]), 5)
            self.assertEqual(state["best_score"], 0)
            self.assertEqual(state["score_history"], [])

    def test_save_and_load_state_round_trip(self):
        path = self.tmp_path("round-trip-state.json")
        state = {
            "quizzes": [],
            "best_score": 10,
            "score_history": [{"nickname": "kim", "score": 10}],
        }

        save_state(state, path)
        with open(path, encoding="utf-8") as file:
            loaded_file = json.load(file)
        loaded_state = load_state(path)

        self.assertEqual(loaded_file["best_score"], 10)
        self.assertEqual(loaded_state["score_history"][0]["nickname"], "kim")
        self.assertEqual(loaded_state["quizzes"], [])

    def test_load_state_recovers_from_broken_json(self):
        path = self.tmp_path("broken-state.json")
        with open(path, "w", encoding="utf-8") as file:
            file.write("{broken")

        state = load_state(path)

        self.assertEqual(len(state["quizzes"]), 5)
        self.assertEqual(state["best_score"], 0)

    def test_save_state_returns_false_when_path_is_not_writable_file(self):
        directory_path = tempfile.mkdtemp(prefix="quiz-game-directory-")
        state = {"quizzes": [], "best_score": 0, "score_history": []}

        result = save_state(state, directory_path)

        self.assertFalse(result)

    def tmp_path(self, filename):
        import tempfile
        import os

        directory = tempfile.mkdtemp(prefix="quiz-game-test-")
        return os.path.join(directory, filename)


if __name__ == "__main__":
    unittest.main()
