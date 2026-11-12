class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

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
            choice = input("선택: ").strip()

            if choice == "1":
                print("🚧 퀴즈 풀기 기능은 준비 중입니다.")
            elif choice == "2":
                print("🚧 퀴즈 추가 기능은 준비 중입니다.")
            elif choice == "3":
                print("🚧 퀴즈 목록 기능은 준비 중입니다.")
            elif choice == "4":
                print("🚧 점수 확인 기능은 준비 중입니다.")
            elif choice == "5":
                print("👋 프로그램을 종료합니다.")
                break
            else:
                print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
