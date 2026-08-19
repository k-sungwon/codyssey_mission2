# Codyssey Mission 2 - 나만의 퀴즈 게임

Python 콘솔에서 실행되는 퀴즈 게임입니다. 사용자는 닉네임을 입력한 뒤 퀴즈를 풀고, 퀴즈 목록을 확인하고, 새 퀴즈를 등록하고, 퀴즈를 삭제하고, 점수 기록을 볼 수 있습니다.

## 프로젝트 개요

이 프로젝트는 Codyssey 두 번째 미션 수행을 위해 만든 Python 콘솔 프로그램입니다.

목표는 단순히 동작하는 게임을 만드는 것뿐 아니라, Python 기본 문법, 클래스, 파일 입출력, JSON 저장, Git 브랜치와 커밋 흐름을 직접 설명할 수 있도록 구성하는 것입니다.

## 퀴즈 주제 선정 이유

기본 퀴즈는 총 5문제이며, 다음 주제를 각각 1문제씩 포함합니다.

- Python 기초
- 스포츠 상식
- 음악 상식
- 영화 상식
- 경제 상식

하나의 주제만 사용하지 않고 여러 분야를 섞은 이유는 퀴즈 게임이 특정 분야에 고정되지 않고 다양한 주제를 저장하고 관리할 수 있다는 점을 보여주기 위해서입니다.

## 실행 환경

Python 3.10 이상이 필요합니다. 실행 전 아래 명령으로 버전을 확인합니다.

```bash
python3 --version
```

출력 예시:

```text
Python 3.10.x
```

Python 3.9 이하가 출력되면 Python 3.10 이상을 설치한 뒤 실행해야 합니다. `.python-version` 파일에는 이 프로젝트의 기준 버전인 `3.10`을 명시했습니다.

교육장 PC처럼 기본 Python 버전이 3.9이고 설치 권한이 없는 경우에는 Docker로 Python 3.10 환경을 사용할 수 있습니다.

### Docker로 Python 3.10 버전 확인

```bash
docker run --rm -it -v "$PWD":/app -w /app python:3.10 python --version
```

### Docker로 퀴즈 게임 실행

```bash
docker run --rm -it -v "$PWD":/app -w /app python:3.10 python main.py
```

### Docker로 자동 테스트 실행

```bash
docker run --rm -v "$PWD":/app -w /app python:3.10 python -m unittest discover -s tests -v
```

Docker 명령어 공통 옵션:

- `docker run`: Docker 컨테이너를 실행합니다.
- `--rm`: 실행이 끝난 컨테이너를 자동으로 삭제합니다.
- `-it`: 사용자가 직접 입력할 수 있게 합니다. 퀴즈 게임 실행처럼 입력이 필요한 경우 사용합니다.
- `-v "$PWD":/app`: 현재 프로젝트 폴더를 컨테이너 안의 `/app` 폴더로 연결합니다.
- `-w /app`: 컨테이너 안에서 `/app` 폴더를 작업 위치로 사용합니다.
- `python:3.10`: Python 3.10이 설치된 Docker 이미지를 사용합니다.

## 실행 방법

아래 명령으로 프로그램을 실행합니다.

```bash
python3 main.py
```

실행하면 먼저 닉네임을 입력합니다.

```text
닉네임을 입력하세요:
```

그 뒤 홈 메뉴에서 원하는 기능 번호를 선택합니다.

```text
1. 퀴즈 풀기
2. 퀴즈 목록
3. 퀴즈 등록
4. 점수 확인
5. 종료
```

## 기능 목록

- 닉네임 입력
- 홈 메뉴 출력
- 퀴즈 풀기
- 풀 문제 수 선택
- 문제 랜덤 출제
- 힌트 보기
- 힌트 사용 시 점수 차감
- 퀴즈 목록 보기
- 퀴즈 상세 보기
- 목록에서 선택한 문제 바로 풀기
- 퀴즈 등록
- 퀴즈 삭제 (`d2`, `d2 4 5`처럼 여러 번호 삭제 가능)
- 기본 퀴즈 초기화 (`reset`)
- 최고 점수 확인
- 점수 기록 히스토리 확인 (최고점 순 정렬)
- `state.json` 저장과 불러오기
- 데이터 파일 없음 또는 손상 시 기본 데이터 복구
- 모든 주요 입력 화면에서 `home` 입력 시 홈으로 이동
- `Ctrl+C` 입력 시 안내 후 홈으로 이동

## 파일 구조

```text
secondMisson/
├── main.py
├── quiz.py
├── quiz_game.py
├── storage.py
├── data.py
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
├── tests/
│   ├── test_quiz.py
│   ├── test_quiz_game.py
│   └── test_storage.py
└── docs/
    ├── code-flow.md
    ├── screenshots/
    └── superpowers/
        ├── specs/
        └── plans/
```

## 파일별 역할

`main.py`

프로그램 시작점입니다. 닉네임을 입력받고 `QuizGame` 객체를 실행합니다.

`quiz.py`

`Quiz` 클래스를 정의합니다. 문제 하나의 주제, 질문, 선택지, 정답, 힌트, 점수 정보를 관리합니다.

`quiz_game.py`

`QuizGame` 클래스를 정의합니다. 홈 메뉴, 퀴즈 풀이, 목록, 등록, 삭제, 점수 확인 등 전체 게임 흐름을 관리합니다.

`storage.py`

`state.json` 파일 저장과 불러오기를 담당합니다. 파일이 없거나 손상된 경우 기본 퀴즈 데이터로 복구합니다.

`data.py`

처음 실행할 때 사용할 기본 퀴즈 5개를 제공합니다.

## state.json 데이터 설명

`state.json`은 프로젝트 루트에 생성됩니다. 프로그램이 종료되거나 퀴즈를 등록/삭제하거나 점수 기록이 생길 때 저장됩니다.

이 파일은 Git에 커밋하지 않습니다. 사용자 실행 결과에 따라 계속 바뀌는 개인 데이터이기 때문입니다.

예시 구조:

```json
{
  "quizzes": [
    {
      "category": "Python 기초",
      "question": "Python에서 여러 값을 순서대로 저장하는 자료형은?",
      "choices": ["dict", "bool", "list", "str"],
      "answer": 3,
      "hint": "대괄호([])를 사용해 만들 수 있는 자료형입니다.",
      "points": 100,
      "hint_penalty": 30
    }
  ],
  "best_score": 70,
  "score_history": [
    {
      "nickname": "tester",
      "played_at": "2026-08-06 15:20:00",
      "score": 70,
      "total_possible_score": 100,
      "quiz_count": 1,
      "correct_count": 1,
      "used_hint_count": 1
    }
  ]
}
```

## 설계 이유

이 프로젝트는 기능별로 파일을 분리했습니다. 한 파일에 모든 코드를 넣으면 처음에는 편하지만, 기능이 늘어날수록 수정 위치를 찾기 어렵습니다.

그래서 문제 하나의 책임은 `Quiz`, 게임 전체 흐름은 `QuizGame`, 파일 저장과 불러오기는 `storage.py`, 기본 데이터는 `data.py`가 담당하도록 나누었습니다. 이런 방식을 관심사의 분리라고 하며, 유지보수하기 쉬운 구조를 만드는 데 도움이 됩니다.

## 테스트 실행

```bash
python3 -m unittest discover -s tests -v
```

## 코드 흐름 문서

코드 구조와 함수 실행 흐름은 [`docs/code-flow.md`](docs/code-flow.md)에서 확인할 수 있습니다.

## 스크린샷 폴더

제출용 실행 화면 스크린샷은 `docs/screenshots/` 폴더에 저장하면 됩니다.

예시 파일명:

```text
docs/screenshots/menu.png
docs/screenshots/play.png
docs/screenshots/add_quiz.png
docs/screenshots/score.png
docs/screenshots/git_log.png
```

## 퀴즈 목록 명령

퀴즈 목록 화면에서는 다음 입력을 사용할 수 있습니다.

```text
번호 입력: 해당 문제를 풀거나 상세 보기 선택
d번호 입력: 해당 문제 삭제
d번호 번호 번호 입력: 여러 문제 삭제
reset 입력: 기본 퀴즈 5개로 초기화
home 입력: 홈 메뉴로 이동
```

## Git 작업 흐름

기능별 브랜치를 만들고, 기능이 완성될 때마다 의미 있는 커밋을 남겼습니다.

커밋 메시지는 `update`, `fix`, `수정`처럼 모호하게 쓰지 않고, 다음처럼 작업 내용을 드러내는 방식으로 작성했습니다.

```text
Feat: Quiz 클래스 추가
Feat: JSON 저장소 구현
Feat: 랜덤 퀴즈 풀이와 점수 기록 구현
Docs: README 작성
```

브랜치 예시:

```text
feature/base-structure
feature/storage
feature/menu-flow
feature/manage-quizzes
feature/play-quiz
feature/docs
```
