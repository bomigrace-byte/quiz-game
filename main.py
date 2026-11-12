import ui
from quiz_game import QuizGame


def main():
    game = None
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 스트림 종료(Ctrl+D / Ctrl+Z)에도 비정상 종료하지 않는다.
        print()
        ui.warn("입력이 중단되어 프로그램을 종료합니다.")
        if game is not None:
            game.save()
            print("💾 데이터를 저장했습니다.")


if __name__ == "__main__":
    main()
