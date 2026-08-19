from quiz_game import QuizGame


def ask_nickname():
    while True:
        try:
            print("닉네임을 입력하세요")
            nickname = input("> ").strip()
            if nickname:
                return nickname
            print("닉네임은 비워둘 수 없습니다.")
        except KeyboardInterrupt:
            print()
            print("닉네임 입력 중 Ctrl+C가 입력되었습니다. 종료하려면 닉네임 입력 후 홈에서 5번을 선택하세요.")
        except EOFError:
            print()
            print("입력이 종료되어 프로그램을 종료합니다.")
            raise SystemExit


def main():
    nickname = ask_nickname()
    game = QuizGame(nickname)
    game.run()


if __name__ == "__main__":
    main()
