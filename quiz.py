from dataclasses import dataclass


@dataclass
class Quiz:
    category: str
    question: str
    choices: list[str]
    answer: int
    hint: str
    points: int = 100
    hint_penalty: int = 30

    def __post_init__(self):
        if len(self.choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if self.answer < 1 or self.answer > 4:
            raise ValueError("정답 번호는 1부터 4 사이여야 합니다.")
        if self.points <= 0:
            raise ValueError("문제 점수는 1점 이상이어야 합니다.")
        if self.hint_penalty < 0:
            raise ValueError("힌트 차감 점수는 0점 이상이어야 합니다.")

    def is_correct(self, choice_number):
        return self.answer == choice_number

    def to_dict(self):
        return {
            "category": self.category,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
            "points": self.points,
            "hint_penalty": self.hint_penalty,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["category"],
            data["question"],
            data["choices"],
            data["answer"],
            data["hint"],
            data.get("points", 100),
            data.get("hint_penalty", 30),
        )
