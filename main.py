import json
import os

# 데이터 파일은 항상 이 파일과 같은 폴더(프로젝트 루트)에 저장한다.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제와 선택지를 화면에 출력한다."""
        print(f"\n[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 반환한다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


def get_default_quizzes():
    """기본 퀴즈 목록을 Quiz 인스턴스로 만들어 반환한다."""
    return [
        Quiz("Python에서 정수(숫자)를 나타내는 자료형은?",
             ["str", "int", "bool", "list"], 2),
        Quiz("Python에서 '키:값' 쌍으로 데이터를 저장하는 자료형은?",
             ["list", "tuple", "dict", "str"], 3),
        Quiz("반복 횟수가 정해져 있지 않고, 조건이 참인 동안 계속 반복할 때 주로 쓰는 문법은?",
             ["for", "if", "def", "while"], 4),
        Quiz("클래스에서 객체가 생성될 때 자동으로 실행되는 메서드는?",
             ["__init__", "__str__", "__main__", "__call__"], 1),
        Quiz("원격 저장소(GitHub)를 내 컴퓨터로 통째로 복제하는 Git 명령어는?",
             ["git pull", "git push", "git clone", "git init"], 3),
        Quiz("새 브랜치를 만들면서 바로 그 브랜치로 이동하는 명령어는?",
             ["git branch -d", "git checkout -b", "git merge", "git add -A"], 2),
        Quiz("원격 저장소의 최신 변경사항을 내 로컬 저장소로 가져와 합치는 명령어는?",
             ["git pull", "git commit", "git log", "git status"], 1),
    ]


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = get_default_quizzes()  # Quiz 객체들의 리스트
        self.best_score = None                # 최고 점수 (아직 안 풀었으면 None)

    # ---------- 입력 처리 ----------
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

    # ---------- 퀴즈 풀기 ----------
    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for i, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(i)
            answer = self.get_number("정답 입력: ", 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct / total * 100)
        print()
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)
        self.save()

    # ---------- 퀴즈 추가 ----------
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

    # ---------- 퀴즈 목록 ----------
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

    # ---------- 점수 확인 ----------
    def show_score(self):
        """최고 점수를 보여준다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")

    # ---------- 파일 저장 ----------
    def save(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- 메뉴 ----------
    def show_menu(self):
        """메인 메뉴를 출력한다."""
        print()
        print("=" * 40)
        print("    🎯 Python & Git 기초 상식 퀴즈 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self):
        """메뉴를 반복해서 보여주고, 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, 5)

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                print("👋 프로그램을 종료합니다.")
                break


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
