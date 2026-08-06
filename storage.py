import json
import os

from data import get_default_quizzes
from quiz import Quiz


DEFAULT_STATE_PATH = "state.json"


def default_state():
    return {
        "quizzes": [quiz.to_dict() for quiz in get_default_quizzes()],
        "best_score": 0,
        "score_history": [],
    }


def load_state(path=DEFAULT_STATE_PATH):
    if not os.path.exists(path):
        return default_state()

    try:
        with open(path, "r", encoding="utf-8") as file:
            loaded = json.load(file)
        return normalize_state(loaded)
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("저장 파일을 읽는 중 문제가 발생하여 기본 퀴즈 데이터로 복구합니다.")
        return default_state()


def save_state(state, path=DEFAULT_STATE_PATH):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(normalize_state(state), file, ensure_ascii=False, indent=2)
        return True
    except OSError:
        print("저장 파일을 쓰는 중 문제가 발생했습니다. 현재 실행 결과가 저장되지 않을 수 있습니다.")
        return False


def normalize_state(state):
    quizzes = state.get("quizzes", [])
    normalized_quizzes = []

    for quiz in quizzes:
        if isinstance(quiz, Quiz):
            normalized_quizzes.append(quiz.to_dict())
        else:
            normalized_quizzes.append(Quiz.from_dict(quiz).to_dict())

    return {
        "quizzes": normalized_quizzes,
        "best_score": int(state.get("best_score", 0)),
        "score_history": list(state.get("score_history", [])),
    }
