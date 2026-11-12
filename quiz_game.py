import json
import os
import random

from quiz import Quiz
from quiz_data import get_default_quizzes

# 데이터 파일은 항상 프로젝트 루트(이 파일과 같은 폴더)에 저장한다.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 게임 전체(메뉴, 진행, 저장)를 관리하는 클래스"""

    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]

    def __init__(self):
        self.quizzes = []        # Quiz 객체들의 리스트
        self.best_score = None   # 최고 점수 (아직 안 풀었으면 None)
        self.load()              # 저장된 데이터가 있으면 불러온다

    # ========== 실행 / 메뉴 ==========
    def run(self):
        """메뉴를 반복해서 보여주고, 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, len(self.MENU_ITEMS))

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                self.save()
                print("👋 프로그램을 종료합니다.")
                break

    def show_menu(self):
        """메인 메뉴를 출력한다."""
        print()
        print("=" * 40)
        print("    🎯 Python & Git 기초 상식 퀴즈 🎯")
        print("=" * 40)
        for i, name in enumerate(self.MENU_ITEMS, start=1):
            print(f"{i}. {name}")
        print("=" * 40)

    # ========== 입력 처리 ==========
    def read_input(self, prompt):
        """입력을 받아 앞뒤 공백을 제거해서 반환한다."""
        return input(prompt).strip()

    def get_number(self, prompt, min_value, max_value):
        """min_value~max_value 범위의 정수를 입력받을 때까지 반복한다."""
        while True:
            text = self.read_input(prompt)

            if text == "":
                print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            try:
                number = int(text)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not min_value <= number <= max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def get_text(self, prompt):
        """빈 값이 아닌 문자열을 입력받을 때까지 반복한다."""
        while True:
            text = self.read_input(prompt)
            if text:
                return text
            print("⚠️ 빈 값은 입력할 수 없습니다. 다시 입력하세요.")

    # ========== 퀴즈 풀기 ==========
    def play(self):
        """저장된 퀴즈를 출제하고 결과를 기록한다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        available = len(self.quizzes)
        total = self.get_number(f"몇 문제를 풀까요? (1-{available}): ", 1, available)
        # random.sample: 원본은 그대로 두고, total개를 무작위 순서로 뽑는다
        selected = random.sample(self.quizzes, total)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for i, quiz in enumerate(selected, start=1):
            print("-" * 40)
            quiz.display(i)
            answer = self.get_number("정답 입력: ", 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct / total * 100)
        self.show_result(total, correct, score)
        self.update_best_score(score)
        self.save()

    def show_result(self, total, correct, score):
        """한 판의 결과를 출력한다."""
        print()
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)

    def update_best_score(self, score):
        """최고 점수와 비교해서 더 높으면 갱신한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

    # ========== 퀴즈 추가 / 목록 ==========
    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.get_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(self.get_text(f"선택지 {i}: "))
        answer = self.get_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈의 문제를 번호와 함께 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    # ========== 점수 확인 ==========
    def show_score(self):
        """최고 점수를 보여준다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")

    # ========== 파일 저장 / 불러오기 ==========
    def reset_to_default(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def load(self):
        """state.json에서 데이터를 불러온다.
        파일이 없거나 손상되었으면 기본 퀴즈 데이터를 사용한다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("best_score 형식이 잘못되었습니다.")

            self.quizzes = quizzes
            self.best_score = best_score
            best_text = "기록 없음" if best_score is None else f"{best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_text})")

        except FileNotFoundError:
            # 첫 실행: 아직 파일이 없음
            self.reset_to_default()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")

        except (json.JSONDecodeError, KeyError, TypeError, AttributeError, ValueError):
            # 파일 내용이 깨졌거나 형식이 맞지 않음
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
            self.reset_to_default()
            self.save()

        except OSError:
            # 권한 문제 등으로 파일을 읽을 수 없음
            print("⚠️ 데이터 파일을 읽을 수 없어 기본 퀴즈 데이터로 시작합니다.")
            self.reset_to_default()

    def save(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠️ 데이터를 저장하지 못했습니다. (파일 쓰기 오류)")
