# 🎯 Python & Git 기초 상식 퀴즈

## 1. 프로젝트 개요

터미널에서 동작하는 **4지선다 퀴즈 게임**입니다.
메뉴에서 번호를 선택해 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록, 점수 확인, 퀴즈 삭제를 할 수 있습니다.
퀴즈와 최고 점수, 게임 기록은 `state.json` 파일에 저장되어 **프로그램을 종료했다가 다시 실행해도 유지**됩니다.

- 언어: Python 3.10 이상
- 외부 라이브러리: 없음 (표준 라이브러리 `json`, `os`, `random`, `datetime`, `sys`만 사용)

## 2. 퀴즈 주제 및 선정 이유

- **주제:** Python & Git 기초 상식
- **선정 이유:** 이번 미션의 학습 목표인 Python 기초 문법(자료형, 반복문, 클래스)과 Git 명령어를 퀴즈로 만들어, 게임을 하면서 자연스럽게 복습할 수 있도록 이 주제를 선택했습니다.

## 3. 실행 방법

```bash
git clone https://github.com/<bomigrace-byte>/quiz-game.git
cd quiz-game
python main.py
```

> Windows에서 `python` 명령이 동작하지 않으면 `py main.py`로 실행합니다.

## 4. 기능 목록

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 풀 문제 수를 선택하면 문제를 **무작위 순서**로 출제하고, 정답/오답과 최종 점수를 보여줍니다. 최고 점수를 넘으면 갱신합니다. |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호(1~4), 힌트(선택)를 입력받아 저장합니다. |
| 3 | 퀴즈 목록 | 등록된 문제를 번호와 함께 보여줍니다. 힌트가 있는 문제는 💡로 표시합니다. |
| 4 | 점수 확인 | 최고 점수와 최근 5회 게임 기록(날짜, 정답 수, 힌트 사용 수, 점수)을 보여줍니다. |
| 5 | 퀴즈 삭제 | 번호를 골라 퀴즈를 삭제합니다. (0 입력 또는 n 입력 시 취소) |
| 6 | 종료 | 데이터를 저장하고 종료합니다. |

### 보너스 기능

- **랜덤 출제:** `random.sample`로 매번 다른 순서로 출제합니다.
- **문제 수 선택:** 1문제부터 전체 문제까지 원하는 만큼 풀 수 있습니다.
- **힌트:** 정답 입력 칸에 `h`를 입력하면 힌트를 볼 수 있습니다.
- **퀴즈 삭제:** 삭제 후 바로 파일에 반영합니다.
- **점수 기록 히스토리:** 모든 게임 기록을 날짜/시간과 함께 저장합니다.
- **화면 꾸미기:** 색상, 진행률 막대, 점수별 응원 문구를 표시합니다.

### 점수 계산 규칙

- 100점 만점이며, 문제 1개의 배점은 `100 ÷ 푼 문제 수`입니다.
- 힌트 없이 맞히면 배점 전체, **힌트를 보고 맞히면 배점의 절반**, 틀리면 0점입니다.
- 최종 점수는 반올림한 정수입니다. 푼 문제 수가 달라도 공정하게 비교할 수 있도록 최고 점수는 이 100점 만점 점수로 비교합니다.

### 입력 및 예외 처리

- 숫자 입력은 앞뒤 공백을 제거한 뒤 처리합니다.
- 빈 입력, 숫자가 아닌 입력(`abc`), 범위 밖 숫자(`9`, `0`)는 안내 메시지를 보여주고 다시 입력받습니다.
- `Ctrl+C`(KeyboardInterrupt)나 입력 종료(EOFError)가 발생하면 데이터를 저장하고 안전하게 종료합니다.
- `state.json`이 없으면 기본 퀴즈로 시작하고, 손상되었으면 안내 메시지를 보여준 뒤 기본 퀴즈 데이터로 복구합니다.

## 5. 파일 구조

```
quiz-game/
├── main.py          # 프로그램 시작점. Ctrl+C / EOF 처리
├── quiz.py          # Quiz 클래스: 퀴즈 1문제 (출력, 정답 확인, 딕셔너리 변환)
├── quiz_game.py     # QuizGame 클래스: 메뉴, 입력 처리, 게임 진행, 저장/불러오기
├── quiz_data.py     # 기본 퀴즈 7개 (Quiz 인스턴스)
├── ui.py            # 화면 꾸미기 (색상, 구분선, 진행률 막대)
├── state.json       # 저장 데이터 (실행 시 자동 생성, Git에는 올리지 않음)
├── docs/
│   └── screenshots/ # 실행 화면 캡처
├── .gitignore
└── README.md
```

### 클래스 역할

| 클래스 | 속성 | 주요 메서드 |
|---|---|---|
| `Quiz` | `question`, `choices`, `answer`, `hint` | `display()`, `is_correct()`, `has_hint()`, `to_dict()`, `from_dict()` |
| `QuizGame` | `quizzes`, `best_score`, `history` | `run()`, `show_menu()`, `play()`, `add_quiz()`, `list_quizzes()`, `show_score()`, `delete_quiz()`, `load()`, `save()`, `get_number()` |

## 6. 데이터 파일 설명 (`state.json`)

- **경로:** 프로젝트 루트의 `state.json` (`main.py`와 같은 폴더)
- **역할:** 퀴즈 목록, 최고 점수, 게임 기록을 저장해서 프로그램을 다시 실행해도 데이터가 유지되게 합니다.
- **인코딩:** UTF-8 (`ensure_ascii=False`로 한글을 그대로 저장)
- **생성 시점:** 첫 실행 후 퀴즈를 풀거나, 추가/삭제하거나, 종료할 때 자동으로 만들어집니다.
- `.gitignore`에 등록해서 저장소에는 올리지 않습니다. (실행하는 사람마다 내용이 다르기 때문)

### 스키마

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `quizzes[].hint` | str | 힌트 (없으면 빈 문자열) |
| `best_score` | int 또는 null | 최고 점수 (100점 만점). 아직 풀지 않았으면 `null` |
| `history` | list | 게임 기록 목록 |
| `history[].date` | str | 플레이 날짜/시간 (`YYYY-MM-DD HH:MM`) |
| `history[].total` | int | 푼 문제 수 |
| `history[].correct` | int | 맞힌 문제 수 |
| `history[].hints_used` | int | 힌트 사용 횟수 |
| `history[].score` | int | 점수 |

### 예시

```json
{
  "quizzes": [
    {
      "question": "Python에서 정수(숫자)를 나타내는 자료형은?",
      "choices": ["str", "int", "bool", "list"],
      "answer": 2,
      "hint": "integer(정수)의 줄임말입니다."
    }
  ],
  "best_score": 86,
  "history": [
    {
      "date": "2026-11-12 20:31",
      "total": 7,
      "correct": 6,
      "hints_used": 0,
      "score": 86
    }
  ]
}
```

## 7. 실행 화면

| 메뉴 | 퀴즈 풀기 |
|---|---|
| ![메뉴](docs/screenshots/menu.png) | ![플레이](docs/screenshots/play.png) |

| 퀴즈 추가 | 점수 확인 |
|---|---|
| ![퀴즈 추가](docs/screenshots/add_quiz.png) | ![점수](docs/screenshots/score.png) |
