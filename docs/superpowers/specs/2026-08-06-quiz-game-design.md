# Codyssey Mission 2 Quiz Game Design

## Goal

Build a Python console quiz game for the Codyssey mission. The program should let a user enter a nickname, solve quizzes, view quiz details, register quizzes, delete quizzes, check score history, and exit from the home menu.

The project should also be explainable. The implementation must make it clear why the code is split by responsibility, why classes are used, why `state.json` is used for persistence, and why Git commits and branches are divided by feature.

## Quiz Topics

The default quiz set has five questions:

- Python basics
- Sports knowledge
- Music knowledge
- Movie knowledge
- Economy knowledge

Using multiple topics shows that the quiz game is not tied to one fixed subject. Users can later add their own categories.

## Architecture

```text
secondMisson/
├── main.py
├── quiz.py
├── quiz_game.py
├── storage.py
├── data.py
├── state.json
├── README.md
└── .gitignore
```

- `main.py`: Program entry point. Asks for nickname and starts `QuizGame`.
- `quiz.py`: Defines the `Quiz` class. A `Quiz` represents one question.
- `quiz_game.py`: Defines the `QuizGame` class. It controls menu flow and user interaction.
- `storage.py`: Loads and saves `state.json`.
- `data.py`: Provides the five default quizzes.
- `state.json`: Stores quizzes, best score, and score history.
- `README.md`: Explains overview, topic choices, how to run, features, file structure, and data format.

This follows separation of concerns: each file has one clear responsibility, so the project is easier to read and maintain.

## Classes

### Quiz

`Quiz` represents one quiz question.

Fields:

- `category`: quiz category
- `question`: question text
- `choices`: four answer choices
- `answer`: correct answer number from 1 to 4
- `hint`: hint text
- `points`: base score for the question
- `hint_penalty`: score penalty when a hint is used

Expected methods:

- `is_correct(choice_number)`: returns whether the selected answer is correct
- `to_dict()`: converts the quiz to JSON-ready data
- `from_dict(data)`: creates a quiz from loaded JSON data

### QuizGame

`QuizGame` manages the whole game flow.

Fields:

- `nickname`
- `quizzes`
- `best_score`
- `score_history`

Responsibilities:

- show home menu
- handle number input and `home`
- play random quizzes
- choose quiz count before playing
- show hints and apply hint penalties
- show quiz list and detail
- register new quizzes
- delete quizzes from the list screen
- reset to default quizzes when the user chooses it
- show score history
- request save after data changes

## Home Menu

```text
1. 퀴즈 풀기
2. 퀴즈 목록
3. 퀴즈 등록
4. 점수 확인
5. 종료
```

All major input screens support `home`. Entering `home` returns to the home menu.

`Ctrl+C` should not crash the program. It prints a guide message and returns to the home menu:

```text
Ctrl+C가 입력되었습니다.
프로그램을 종료하려면 홈 화면에서 5번 종료를 선택하세요.
홈으로 돌아갑니다.
```

`EOFError` means input is no longer available, so the app saves data and exits safely.

## Bonus Requirements

All bonus requirements are included:

- Random quiz order
- Choose how many questions to solve
- Hint feature
- Hint score penalty
- Delete quizzes
- Full score history with date, time, quiz count, score, and hint usage

## Empty Quiz State

If the user deletes every quiz, the program keeps the empty state. This is intentional user behavior.

When there are no quizzes, the app provides choices:

```text
현재 등록된 퀴즈가 없습니다.

1. 퀴즈 등록하러 가기
2. 기본 퀴즈로 초기화하기
home. 처음으로 돌아가기
```

If `state.json` is missing or broken, that is treated as an error state, so the app restores the default quizzes.

## Score History

Only completed quiz sessions are recorded. If the user enters `home` during a quiz session, no score history entry is saved.

Score history fields:

- nickname
- played_at
- score
- total_possible_score
- quiz_count
- correct_count
- used_hint_count

## state.json Schema

```json
{
  "quizzes": [
    {
      "category": "Python 기초",
      "question": "Python에서 리스트를 만드는 기호는?",
      "choices": ["()", "[]", "{}", "<>"],
      "answer": 2,
      "hint": "여러 값을 순서대로 저장할 때 쓰는 괄호입니다.",
      "points": 100,
      "hint_penalty": 30
    }
  ],
  "best_score": 0,
  "score_history": []
}
```

## Git Strategy

Use meaningful commits. A meaningful commit explains the unit of work.

Bad examples:

- `update`
- `fix`
- `수정`
- `asdf`

Good examples:

- `Feat: Quiz 클래스 추가`
- `Feat: 퀴즈 등록 기능 구현`
- `Fix: Ctrl+C 홈 복귀 처리`
- `Docs: README 실행 방법 추가`

Use feature branches and merge them back into `main`.

Planned branch flow:

- `feature/base-structure`
- `feature/storage`
- `feature/manage-quizzes`
- `feature/play-quiz`
- `feature/score-history`
- `feature/docs`

Planned commits:

1. `Docs: 퀴즈 게임 설계 문서 작성`
2. `Docs: 구현 계획 문서 작성`
3. `Init: 프로젝트 기본 파일 추가`
4. `Feat: Quiz 클래스 추가`
5. `Feat: 기본 퀴즈 데이터 추가`
6. `Feat: JSON 저장소 구현`
7. `Feat: 홈 메뉴와 공통 입력 처리 구현`
8. `Feat: 퀴즈 목록과 상세 보기 구현`
9. `Feat: 퀴즈 등록 기능 구현`
10. `Feat: 퀴즈 삭제 기능 구현`
11. `Feat: 랜덤 퀴즈 풀이와 힌트 기능 구현`
12. `Feat: 점수 기록 히스토리 구현`
13. `Fix: 예외 처리와 홈 이동 흐름 보강`
14. `Docs: README 작성`

