class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

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
