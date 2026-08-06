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
        print("퀴즈 풀기 기능을 준비 중입니다.")

    def show_quiz_list(self):
        print("퀴즈 목록 기능을 준비 중입니다.")

    def add_quiz(self):
        print("퀴즈 등록 기능을 준비 중입니다.")

    def show_scores(self):
        print("점수 확인 기능을 준비 중입니다.")

    def save(self):
        self.state["quizzes"] = [quiz.to_dict() for quiz in self.quizzes]
        self.state["best_score"] = self.best_score
        self.state["score_history"] = self.score_history
        save_state(self.state, self.state_path)
