import random
from datetime import datetime

from quiz import Quiz
from storage import DEFAULT_STATE_PATH, load_state, save_state


HOME = "home"


class QuizGame:
    def __init__(self, nickname, state_path=DEFAULT_STATE_PATH):
        self.nickname = nickname
        self.state_path = state_path
        self.state = load_state(state_path)
        self.quizzes = [Quiz.from_dict(quiz) for quiz in self.state["quizzes"]]
        self.best_score = self.state["best_score"]
        self.score_history = self.state["score_history"]

    @staticmethod
    def parse_number(raw_value, min_value, max_value):
        value = raw_value.strip()
        if value.lower() == HOME:
            return HOME
        if value == "":
            return None
        try:
            number = int(value)
        except ValueError:
            return None
        if number < min_value or number > max_value:
            return None
        return number

    @staticmethod
    def parse_delete_command(raw_value, quiz_count):
        value = raw_value.strip().lower()
        if not value.startswith("d"):
            return None
        number_text = value[1:].strip()
        if not number_text:
            return None
        try:
            number = int(number_text)
        except ValueError:
            return None
        if number < 1 or number > quiz_count:
            return None
        return number

    def get_number(self, prompt, min_value, max_value):
        while True:
            raw_value = input(prompt)
            result = self.parse_number(raw_value, min_value, max_value)
            if result is not None:
                return result
            print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")

    def run(self):
        while True:
            try:
                choice = self.show_home()
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.show_quiz_list()
                elif choice == 3:
                    self.add_quiz()
                elif choice == 4:
                    self.show_scores()
                elif choice == 5:
                    self.save()
                    print("프로그램을 종료합니다.")
                    break
            except KeyboardInterrupt:
                print()
                print("Ctrl+C가 입력되었습니다.")
                print("프로그램을 종료하려면 홈 화면에서 5번 종료를 선택하세요.")
                print("홈으로 돌아갑니다.")
            except EOFError:
                print()
                print("입력 스트림이 종료되어 데이터를 저장하고 프로그램을 종료합니다.")
                self.save()
                break

    def show_home(self):
        print()
        print("=" * 40)
        print("나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 목록")
        print("3. 퀴즈 등록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)
        return self.get_number("선택: ", 1, 5)

    def play_quiz(self):
        if self.handle_empty_quizzes():
            return

        print()
        print(f"현재 등록된 퀴즈는 {len(self.quizzes)}개입니다.")
        quiz_count = self.get_number(f"몇 문제를 풀까요? (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        if quiz_count == HOME:
            return

        selected_quizzes = random.sample(self.quizzes, quiz_count)
        score = 0
        total_possible_score = sum(quiz.points for quiz in selected_quizzes)
        correct_count = 0
        used_hint_count = 0

        print()
        print(f"퀴즈를 시작합니다. 총 {quiz_count}문제입니다.")

        for index, quiz in enumerate(selected_quizzes, start=1):
            used_hint = False
            print()
            print("-" * 40)
            print(f"[문제 {index}] {quiz.category}")
            print(quiz.question)
            for choice_index, choice in enumerate(quiz.choices, start=1):
                print(f"{choice_index}. {choice}")
            print(f"h. 힌트 보기 (-{quiz.hint_penalty}점)")
            print("home. 처음으로 돌아가기")

            while True:
                raw_answer = input("정답 입력: ").strip().lower()
                if raw_answer == HOME:
                    print("풀이를 중단하고 홈으로 돌아갑니다. 점수 기록은 저장하지 않습니다.")
                    return
                if raw_answer == "h":
                    if used_hint:
                        print("이미 힌트를 사용했습니다.")
                    else:
                        used_hint = True
                        used_hint_count += 1
                        print(f"힌트: {quiz.hint} (-{quiz.hint_penalty}점)")
                    continue

                answer = self.parse_number(raw_answer, 1, 4)
                if answer is None:
                    print("잘못된 입력입니다. 1-4 사이 숫자, h, home 중 하나를 입력하세요.")
                    continue

                correct = quiz.is_correct(answer)
                earned = self.calculate_question_score(quiz, used_hint, correct)
                score += earned
                if correct:
                    correct_count += 1
                    print(f"정답입니다! +{earned}점")
                else:
                    print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
                break

        self.record_score(score, total_possible_score, quiz_count, correct_count, used_hint_count)
        print()
        print("=" * 40)
        print(f"결과: {quiz_count}문제 중 {correct_count}문제 정답")
        print(f"점수: {score}/{total_possible_score}점")
        print(f"힌트 사용: {used_hint_count}회")
        print(f"최고 점수: {self.best_score}점")
        print("=" * 40)

    def show_quiz_list(self):
        while True:
            if self.handle_empty_quizzes():
                return

            print()
            print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
            print("-" * 40)
            for index, quiz in enumerate(self.quizzes, start=1):
                print(f"{index}. {quiz.category} - {quiz.question}")
            print("-" * 40)
            print("상세히 볼 퀴즈 번호를 입력하세요.")
            print("삭제하려면 d번호를 입력하세요. 예: d2")
            print("home 입력 시 처음으로 돌아갑니다.")

            raw_value = input("입력: ")
            if raw_value.strip().lower() == HOME:
                return

            delete_number = self.parse_delete_command(raw_value, len(self.quizzes))
            if delete_number is not None:
                self.delete_quiz(delete_number)
                continue

            detail_number = self.parse_number(raw_value, 1, len(self.quizzes))
            if detail_number is None:
                print("잘못된 입력입니다. 번호, d번호, home 중 하나를 입력하세요.")
                continue
            self.show_quiz_detail(detail_number)

    def add_quiz(self):
        print()
        print("새로운 퀴즈를 등록합니다. home 입력 시 처음으로 돌아갑니다.")

        category = self.get_text("주제: ")
        if category == HOME:
            return
        question = self.get_text("문제: ")
        if question == HOME:
            return

        choices = []
        for index in range(1, 5):
            choice = self.get_text(f"선택지 {index}: ")
            if choice == HOME:
                return
            choices.append(choice)

        answer = self.get_number("정답 번호 (1-4): ", 1, 4)
        if answer == HOME:
            return

        hint = self.get_text("힌트: ")
        if hint == HOME:
            return

        points = self.get_number("문제 점수 (1-1000): ", 1, 1000)
        if points == HOME:
            return

        hint_penalty = self.get_number("힌트 차감 점수 (0-1000): ", 0, 1000)
        if hint_penalty == HOME:
            return

        quiz = Quiz(category, question, choices, answer, hint, points, hint_penalty)
        self.quizzes.append(quiz)
        self.save()
        print("퀴즈가 등록되었습니다.")

    def show_scores(self):
        print()
        print("점수 기록")
        print("-" * 40)
        if not self.score_history:
            print("아직 완료한 퀴즈 기록이 없습니다.")
            return

        print(f"최고 점수: {self.best_score}점")
        for index, record in enumerate(self.score_history, start=1):
            print()
            print(f"[{index}] {record['played_at']}")
            print(f"닉네임: {record['nickname']}")
            print(f"점수: {record['score']}/{record['total_possible_score']}점")
            print(f"푼 문제 수: {record['quiz_count']}개")
            print(f"정답 수: {record['correct_count']}개")
            print(f"힌트 사용 수: {record['used_hint_count']}회")

    def save(self):
        self.state["quizzes"] = [quiz.to_dict() for quiz in self.quizzes]
        self.state["best_score"] = self.best_score
        self.state["score_history"] = self.score_history
        save_state(self.state, self.state_path)

    def get_text(self, prompt):
        while True:
            value = input(prompt).strip()
            if value.lower() == HOME:
                return HOME
            if value:
                return value
            print("빈 입력은 사용할 수 없습니다.")

    def show_quiz_detail(self, quiz_number):
        quiz = self.quizzes[quiz_number - 1]
        print()
        print(f"[{quiz_number}] {quiz.category}")
        print(quiz.question)
        for index, choice in enumerate(quiz.choices, start=1):
            print(f"{index}. {choice}")
        print(f"정답: {quiz.answer}")
        print(f"힌트: {quiz.hint}")
        print(f"점수: {quiz.points}점 / 힌트 차감: {quiz.hint_penalty}점")

    def delete_quiz(self, quiz_number):
        quiz = self.quizzes[quiz_number - 1]
        confirm = input(f"'{quiz.question}' 퀴즈를 정말 삭제하시겠습니까? (y/n): ").strip().lower()
        if confirm != "y":
            print("삭제를 취소했습니다.")
            return
        del self.quizzes[quiz_number - 1]
        self.save()
        print("퀴즈가 삭제되었습니다.")

    def handle_empty_quizzes(self):
        if self.quizzes:
            return False

        while True:
            print()
            print("현재 등록된 퀴즈가 없습니다.")
            print("1. 퀴즈 등록하러 가기")
            print("2. 기본 퀴즈로 초기화하기")
            print("home. 처음으로 돌아가기")
            choice = self.get_number("선택: ", 1, 2)
            if choice == HOME:
                return True
            if choice == 1:
                self.add_quiz()
                return True
            if choice == 2:
                from data import get_default_quizzes

                self.quizzes = get_default_quizzes()
                self.save()
                print("기본 퀴즈로 초기화했습니다.")
                return False

    @staticmethod
    def calculate_question_score(quiz, used_hint, correct):
        if not correct:
            return 0
        if used_hint:
            return max(0, quiz.points - quiz.hint_penalty)
        return quiz.points

    def record_score(self, score, total_possible_score, quiz_count, correct_count, used_hint_count):
        record = {
            "nickname": self.nickname,
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "total_possible_score": total_possible_score,
            "quiz_count": quiz_count,
            "correct_count": correct_count,
            "used_hint_count": used_hint_count,
        }
        self.score_history.append(record)
        if score > self.best_score:
            self.best_score = score
        self.save()
