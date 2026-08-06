# Quiz Game Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Codyssey Python console quiz game with all required features and all bonus features.

**Architecture:** The app is split by responsibility: `Quiz` models one question, `QuizGame` controls user flow, `storage.py` handles JSON persistence, and `data.py` owns default quizzes. The app stores all persistent data in root-level `state.json`.

**Tech Stack:** Python 3.10+, standard library only, JSON file persistence, Git feature branches.

## Global Constraints

- Use Python 3.10 or higher.
- Use only the Python standard library.
- Store persistent data in project-root `state.json`.
- Read and write JSON using UTF-8 encoding.
- Define at least two classes.
- Support quiz solving, quiz adding, quiz listing, score checking, and exit.
- Include at least five default quizzes.
- Include all bonus features: random questions, quiz count selection, hints, hint penalties, quiz deletion, and score history.
- Support `home` on major input screens.
- Handle empty input, non-number input, out-of-range numbers, `KeyboardInterrupt`, and `EOFError`.

---

## File Map

- `main.py`: entry point; nickname input; starts `QuizGame`.
- `quiz.py`: `Quiz` class.
- `data.py`: default quiz data factory.
- `storage.py`: `load_state`, `save_state`, and state normalization.
- `quiz_game.py`: `QuizGame` class and all menu flows.
- `tests/test_quiz.py`: unit tests for `Quiz`.
- `tests/test_storage.py`: unit tests for storage behavior.
- `tests/test_quiz_game.py`: focused tests for score calculations and empty-state helpers.
- `README.md`: final mission documentation.
- `.gitignore`: Python and local runtime ignores.

### Task 1: Add Project Scaffold

**Files:**
- Create: `.gitignore`
- Create: `main.py`
- Create: `quiz.py`
- Create: `data.py`
- Create: `storage.py`
- Create: `quiz_game.py`
- Create: `tests/test_quiz.py`
- Create: `tests/test_storage.py`
- Create: `tests/test_quiz_game.py`

**Interfaces:**
- Produces empty files that later tasks fill.

- [ ] **Step 1: Create branch**

```bash
git checkout -b feature/base-structure
```

- [ ] **Step 2: Add scaffold files**

Create empty Python modules and tests. Add `.gitignore` with:

```gitignore
__pycache__/
*.pyc
.pytest_cache/
state.json
.DS_Store
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore main.py quiz.py data.py storage.py quiz_game.py tests
git commit -m "Init: 프로젝트 기본 파일 추가"
```

### Task 2: Implement Quiz Class

**Files:**
- Modify: `quiz.py`
- Modify: `tests/test_quiz.py`

**Interfaces:**
- Produces: `Quiz(category: str, question: str, choices: list[str], answer: int, hint: str, points: int = 100, hint_penalty: int = 30)`
- Produces: `Quiz.is_correct(choice_number: int) -> bool`
- Produces: `Quiz.to_dict() -> dict`
- Produces: `Quiz.from_dict(data: dict) -> Quiz`

- [ ] **Step 1: Write failing tests**

```python
from quiz import Quiz


def test_quiz_checks_correct_answer():
    quiz = Quiz("Python 기초", "리스트 기호는?", ["()", "[]", "{}", "<>"], 2, "대괄호")
    assert quiz.is_correct(2) is True
    assert quiz.is_correct(1) is False


def test_quiz_converts_to_and_from_dict():
    quiz = Quiz("경제 상식", "수요가 늘면?", ["가격 상승", "항상 하락", "변화 없음", "폐지"], 1, "시장 가격", 100, 30)
    restored = Quiz.from_dict(quiz.to_dict())
    assert restored.category == "경제 상식"
    assert restored.choices[0] == "가격 상승"
    assert restored.answer == 1
```

- [ ] **Step 2: Run failing tests**

```bash
python -m pytest tests/test_quiz.py -v
```

- [ ] **Step 3: Implement `Quiz`**

Use `@dataclass`. Validate that choices has four items and answer is 1-4.

- [ ] **Step 4: Run passing tests**

```bash
python -m pytest tests/test_quiz.py -v
```

- [ ] **Step 5: Commit**

```bash
git add quiz.py tests/test_quiz.py
git commit -m "Feat: Quiz 클래스 추가"
```

### Task 3: Add Default Quiz Data

**Files:**
- Modify: `data.py`
- Modify: `tests/test_quiz.py`

**Interfaces:**
- Consumes: `Quiz`
- Produces: `get_default_quizzes() -> list[Quiz]`

- [ ] **Step 1: Write failing test**

```python
from data import get_default_quizzes


def test_default_quizzes_have_five_topics():
    quizzes = get_default_quizzes()
    categories = {quiz.category for quiz in quizzes}
    assert len(quizzes) == 5
    assert {"Python 기초", "스포츠 상식", "음악 상식", "영화 상식", "경제 상식"} == categories
```

- [ ] **Step 2: Run failing test**

```bash
python -m pytest tests/test_quiz.py -v
```

- [ ] **Step 3: Implement default quizzes**

Create one quiz for each agreed topic. Each quiz has four choices, answer 1-4, hint, `points=100`, and `hint_penalty=30`.

- [ ] **Step 4: Run passing tests**

```bash
python -m pytest tests/test_quiz.py -v
```

- [ ] **Step 5: Commit**

```bash
git add data.py tests/test_quiz.py
git commit -m "Feat: 기본 퀴즈 데이터 추가"
```

### Task 4: Implement JSON Storage

**Files:**
- Modify: `storage.py`
- Modify: `tests/test_storage.py`

**Interfaces:**
- Consumes: `Quiz`, `get_default_quizzes`
- Produces: `load_state(path: str = "state.json") -> dict`
- Produces: `save_state(state: dict, path: str = "state.json") -> None`

- [ ] **Step 1: Merge base branch and create storage branch**

```bash
git checkout main
git merge feature/base-structure
git checkout -b feature/storage
```

- [ ] **Step 2: Write failing tests**

```python
import json

from storage import load_state, save_state


def test_load_state_uses_defaults_when_file_missing(tmp_path):
    state = load_state(str(tmp_path / "state.json"))
    assert len(state["quizzes"]) == 5
    assert state["best_score"] == 0
    assert state["score_history"] == []


def test_save_and_load_state_round_trip(tmp_path):
    path = tmp_path / "state.json"
    state = {"quizzes": [], "best_score": 10, "score_history": [{"nickname": "kim"}]}
    save_state(state, str(path))
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["best_score"] == 10
    assert load_state(str(path))["score_history"][0]["nickname"] == "kim"


def test_load_state_recovers_from_broken_json(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("{broken", encoding="utf-8")
    state = load_state(str(path))
    assert len(state["quizzes"]) == 5
```

- [ ] **Step 3: Run failing tests**

```bash
python -m pytest tests/test_storage.py -v
```

- [ ] **Step 4: Implement storage**

Store quizzes as dictionaries. Preserve an empty quiz list if it was saved intentionally.

- [ ] **Step 5: Run passing tests**

```bash
python -m pytest tests/test_storage.py -v
```

- [ ] **Step 6: Commit storage and merge**

```bash
git add storage.py tests/test_storage.py
git commit -m "Feat: JSON 저장소 구현"
git checkout main
git merge feature/storage
```

### Task 5: Implement Home Menu and Input Helpers

**Files:**
- Modify: `quiz_game.py`
- Modify: `main.py`

**Interfaces:**
- Consumes: `load_state`, `save_state`, `Quiz`
- Produces: `QuizGame.run() -> None`
- Produces: `QuizGame.get_number(prompt: str, min_value: int, max_value: int) -> int | str`

- [ ] **Step 1: Implement base `QuizGame`**

Create constructor that receives `nickname`, loads state, and stores quiz objects.

- [ ] **Step 2: Implement home menu**

Implement options 1-5. For unfinished options, print a short preparing message until later tasks fill them.

- [ ] **Step 3: Implement input helper**

`get_number` strips input, accepts `home`, rejects empty input, non-numbers, and out-of-range numbers.

- [ ] **Step 4: Implement interrupt behavior**

Catch `KeyboardInterrupt` in `run`, print the Ctrl+C guide, and return to home. Catch `EOFError`, save, and exit safely.

- [ ] **Step 5: Commit**

```bash
git checkout -b feature/menu-flow
git add main.py quiz_game.py
git commit -m "Feat: 홈 메뉴와 공통 입력 처리 구현"
git checkout main
git merge feature/menu-flow
```

### Task 6: Implement Quiz List, Detail, Add, and Delete

**Files:**
- Modify: `quiz_game.py`

**Interfaces:**
- Consumes: `Quiz`
- Produces: `QuizGame.show_quiz_list() -> None`
- Produces: `QuizGame.add_quiz() -> None`

- [ ] **Step 1: Create branch**

```bash
git checkout -b feature/manage-quizzes
```

- [ ] **Step 2: Implement quiz list and detail**

Show quiz count, category, question summary, detail by number, and `home`.

- [ ] **Step 3: Commit list feature**

```bash
git add quiz_game.py
git commit -m "Feat: 퀴즈 목록과 상세 보기 구현"
```

- [ ] **Step 4: Implement quiz registration**

Ask category, question, four choices, answer number, hint, points, and hint penalty. Save after adding.

- [ ] **Step 5: Commit add feature**

```bash
git add quiz_game.py
git commit -m "Feat: 퀴즈 등록 기능 구현"
```

- [ ] **Step 6: Implement delete through list screen**

Accept `d번호`, ask `정말 삭제하시겠습니까? (y/n):`, delete, and save.

- [ ] **Step 7: Commit delete feature and merge**

```bash
git add quiz_game.py
git commit -m "Feat: 퀴즈 삭제 기능 구현"
git checkout main
git merge feature/manage-quizzes
```

### Task 7: Implement Play Quiz, Hints, and Score History

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `QuizGame.play_quiz() -> None`
- Produces: `QuizGame.calculate_question_score(quiz: Quiz, used_hint: bool, correct: bool) -> int`
- Produces: `QuizGame.record_score(score: int, total_possible_score: int, quiz_count: int, correct_count: int, used_hint_count: int) -> None`

- [ ] **Step 1: Write score helper tests**

```python
from quiz import Quiz
from quiz_game import QuizGame


def test_question_score_applies_hint_penalty_only_when_correct():
    quiz = Quiz("Python 기초", "리스트?", ["()", "[]", "{}", "<>"], 2, "대괄호", 100, 30)
    assert QuizGame.calculate_question_score(quiz, used_hint=False, correct=True) == 100
    assert QuizGame.calculate_question_score(quiz, used_hint=True, correct=True) == 70
    assert QuizGame.calculate_question_score(quiz, used_hint=True, correct=False) == 0
```

- [ ] **Step 2: Run failing test**

```bash
python -m pytest tests/test_quiz_game.py -v
```

- [ ] **Step 3: Create branch**

```bash
git checkout -b feature/play-quiz
```

- [ ] **Step 4: Implement quiz playing**

Let users choose quiz count. Use `random.sample` to select quizzes. Support answer number, `h` for hint, and `home`.

- [ ] **Step 5: Implement score recording**

Record nickname, timestamp, score, total possible score, quiz count, correct count, and hint count. Update `best_score`.

- [ ] **Step 6: Run tests and commit**

```bash
python -m pytest -v
git add quiz_game.py tests/test_quiz_game.py
git commit -m "Feat: 랜덤 퀴즈 풀이와 힌트 기능 구현"
git add quiz_game.py
git commit -m "Feat: 점수 기록 히스토리 구현"
git checkout main
git merge feature/play-quiz
```

### Task 8: Final Exception Pass and README

**Files:**
- Modify: `quiz_game.py`
- Modify: `README.md`

**Interfaces:**
- Completes user-facing documentation and mission checklist.

- [ ] **Step 1: Create docs branch**

```bash
git checkout -b feature/docs
```

- [ ] **Step 2: Verify exception flows**

Manually test empty input, `abc`, out-of-range number, `home`, no quizzes, and Ctrl+C.

- [ ] **Step 3: Commit fixes if needed**

```bash
git add quiz_game.py
git commit -m "Fix: 예외 처리와 홈 이동 흐름 보강"
```

- [ ] **Step 4: Write README**

Include project overview, topic reason, run method, feature list, file structure, and `state.json` schema.

- [ ] **Step 5: Commit README and merge**

```bash
git add README.md
git commit -m "Docs: README 작성"
git checkout main
git merge feature/docs
```

### Task 9: Final Verification and Push

**Files:**
- Read: all project files

**Interfaces:**
- Produces final evidence for submission.

- [ ] **Step 1: Run tests**

```bash
python -m pytest -v
```

- [ ] **Step 2: Run console smoke test**

```bash
python main.py
```

- [ ] **Step 3: Check Git history**

```bash
git log --oneline --graph --decorate --all
```

- [ ] **Step 4: Push**

```bash
git push origin main
```
