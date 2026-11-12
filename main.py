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
                print("🚧 퀴즈 풀기 기능은 준비 중입니다.")
            elif choice == 2:
                print("🚧 퀴즈 추가 기능은 준비 중입니다.")
            elif choice == 3:
                print("🚧 퀴즈 목록 기능은 준비 중입니다.")
            elif choice == 4:
                print("🚧 점수 확인 기능은 준비 중입니다.")
            else:
                print("👋 프로그램을 종료합니다.")
                break


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
