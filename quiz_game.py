import json
import os
import random
from datetime import datetime

import ui
from backup import BackupManager
from quiz import Quiz
from quiz_data import get_default_quizzes

# 데이터 파일은 항상 프로젝트 루트(이 파일과 같은 폴더)에 저장한다.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 게임 전체(메뉴, 진행, 저장)를 관리하는 클래스"""

    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "퀴즈 삭제", "종료"]
    RECENT_HISTORY_COUNT = 5  # 점수 확인 화면에 보여줄 최근 기록 개수

    def __init__(self):
        self.quizzes = []        # Quiz 객체들의 리스트
        self.best_score = None   # 최고 점수 (아직 안 풀었으면 None)
        self.history = []        # 게임 기록 리스트 (딕셔너리들)
        self.backup = BackupManager(STATE_FILE)  # 백업/복구 담당
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
            elif choice == 5:
                self.delete_quiz()
            else:
                self.save()
                print("👋 프로그램을 종료합니다.")
                break

    def show_menu(self):
        """메인 메뉴를 출력한다."""
        print()
        ui.title("🎯 Python & Git 기초 상식 퀴즈 🎯")
        for i, name in enumerate(self.MENU_ITEMS, start=1):
            number = ui.color(str(i), ui.BOLD, ui.YELLOW)
            print(f"  {number}. {name}")
        ui.line("═")

    # ========== 입력 처리 ==========
    def read_input(self, prompt):
        """입력을 받아 앞뒤 공백을 제거해서 반환한다."""
        return input(prompt).strip()

    def get_number(self, prompt, min_value, max_value):
        """min_value~max_value 범위의 정수를 입력받을 때까지 반복한다."""
        while True:
            text = self.read_input(prompt)

            if text == "":
                ui.warn(f"입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            try:
                number = int(text)
            except ValueError:
                ui.warn(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not min_value <= number <= max_value:
                ui.warn(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def get_text(self, prompt):
        """빈 값이 아닌 문자열을 입력받을 때까지 반복한다."""
        while True:
            text = self.read_input(prompt)
            if text:
                return text
            ui.warn("빈 값은 입력할 수 없습니다. 다시 입력하세요.")

    def ask_yes_no(self, prompt):
        """y 또는 n을 입력받아 y이면 True를 반환한다."""
        while True:
            text = self.read_input(prompt).lower()
            if text == "y":
                return True
            if text == "n":
                return False
            ui.warn("y 또는 n을 입력하세요.")

    def get_answer(self, quiz):
        """정답 번호(1~4)를 입력받는다. 'h'를 입력하면 힌트를 보여준다.
        (정답 번호, 힌트 사용 여부)를 반환한다."""
        used_hint = False
        while True:
            if quiz.has_hint():
                text = self.read_input("정답 입력 (1-4, 힌트는 h): ").lower()
            else:
                text = self.read_input("정답 입력 (1-4): ").lower()

            if text == "":
                ui.warn("입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.")
                continue

            if text == "h" and quiz.has_hint():
                if used_hint:
                    ui.info("이미 힌트를 확인했습니다.")
                else:
                    used_hint = True
                    ui.info(f"힌트: {quiz.hint}")
                    print(ui.color("   (힌트를 본 문제는 맞혀도 절반 점수만 받습니다)", ui.DIM))
                continue

            try:
                number = int(text)
            except ValueError:
                ui.warn("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                continue

            if not 1 <= number <= 4:
                ui.warn("잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                continue

            return number, used_hint

    # ========== 퀴즈 풀기 ==========
    def play(self):
        """저장된 퀴즈를 출제하고 결과를 기록한다."""
        if not self.quizzes:
            ui.warn("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        available = len(self.quizzes)
        total = self.get_number(f"몇 문제를 풀까요? (1-{available}): ", 1, available)
        # random.sample: 원본은 그대로 두고, total개를 무작위 순서로 뽑는다
        selected = random.sample(self.quizzes, total)
        correct = 0
        hints_used = 0
        earned = 0                    # 획득 점수 (소수점 포함)
        per_question = 100 / total    # 문제 1개의 배점
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for i, quiz in enumerate(selected, start=1):
            ui.line()
            ui.progress(i, total)
            quiz.display(i)
            answer, used_hint = self.get_answer(quiz)
            if used_hint:
                hints_used += 1

            if quiz.is_correct(answer):
                correct += 1
                if used_hint:
                    earned += per_question / 2   # 힌트 사용 시 절반 점수
                else:
                    earned += per_question
                ui.success("정답입니다!")
            else:
                ui.error(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(earned)
        self.show_result(total, correct, hints_used, score)
        self.add_history(total, correct, hints_used, score)
        self.update_best_score(score)
        self.save()

    def show_result(self, total, correct, hints_used, score):
        """한 판의 결과를 출력한다."""
        print()
        ui.title(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hints_used > 0:
            ui.info(f"힌트 사용: {hints_used}회 (힌트 사용 문제는 절반 점수)")
        print(ui.score_message(score))

    def add_history(self, total, correct, hints_used, score):
        """이번 게임 기록을 히스토리에 추가한다."""
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total": total,
            "correct": correct,
            "hints_used": hints_used,
            "score": score,
        }
        self.history.append(record)

    def update_best_score(self, score):
        """최고 점수와 비교해서 더 높으면 갱신한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print(ui.color("🎉 새로운 최고 점수입니다!", ui.BOLD, ui.GREEN))

    # ========== 퀴즈 추가 / 목록 ==========
    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.get_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(self.get_text(f"선택지 {i}: "))
        answer = self.get_number("정답 번호 (1-4): ", 1, 4)
        hint = self.read_input("힌트 (없으면 Enter): ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save()
        print()
        ui.success("퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈의 문제를 번호와 함께 보여준다."""
        if not self.quizzes:
            ui.warn("등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        ui.line()
        for i, quiz in enumerate(self.quizzes, start=1):
            hint_mark = " 💡" if quiz.has_hint() else ""
            print(f"[{i}] {quiz.question}{hint_mark}")
        ui.line()

    def delete_quiz(self):
        """번호를 골라 퀴즈를 삭제하고 파일에 반영한다."""
        if not self.quizzes:
            ui.warn("삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        total = len(self.quizzes)
        number = self.get_number(f"삭제할 퀴즈 번호 (1-{total}, 취소는 0): ", 0, total)
        if number == 0:
            print("↩️ 삭제를 취소했습니다.")
            return

        target = self.quizzes[number - 1]  # 화면 번호는 1부터, 리스트 인덱스는 0부터
        if self.ask_yes_no(f"'{target.question}' 퀴즈를 삭제할까요? (y/n): "):
            self.quizzes.pop(number - 1)
            self.save()
            ui.success("퀴즈가 삭제되었습니다.")
        else:
            print("↩️ 삭제를 취소했습니다.")

    # ========== 점수 확인 ==========
    def show_score(self):
        """최고 점수와 최근 게임 기록을 보여준다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요!")
            return
        print()
        print(ui.color(f"🏆 최고 점수: {self.best_score}점", ui.BOLD, ui.YELLOW))

        if not self.history:
            return
        recent = self.history[-self.RECENT_HISTORY_COUNT:]
        print(f"\n📜 최근 게임 기록 (총 {len(self.history)}회 중 최근 {len(recent)}회)")
        ui.line()
        for record in reversed(recent):  # 최신 기록부터 출력
            print(f"{record.get('date', '-')} | "
                  f"{record.get('correct', 0)}/{record.get('total', 0)} 정답 | "
                  f"힌트 {record.get('hints_used', 0)}회 | "
                  f"{record.get('score', 0)}점")
        ui.line()

    # ========== 파일 저장 / 불러오기 ==========
    def reset_to_default(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.history = []

    def read_state(self, path):
        """데이터 파일을 읽어 (퀴즈 목록, 최고 점수, 기록)을 반환한다.
        파일이 없거나 형식이 잘못되었으면 예외가 그대로 발생한다."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        best_score = data.get("best_score")
        if best_score is not None and not isinstance(best_score, int):
            raise ValueError("best_score 형식이 잘못되었습니다.")
        history = data.get("history", [])  # 예전 파일에는 history가 없을 수 있다
        if not isinstance(history, list) or not all(isinstance(r, dict) for r in history):
            raise ValueError("history 형식이 잘못되었습니다.")

        return quizzes, best_score, history

    def load(self):
        """state.json에서 데이터를 불러온다.
        파일이 없으면 기본 퀴즈 데이터를 쓰고, 손상되었으면 복구 절차를 진행한다."""
        try:
            quizzes, best_score, history = self.read_state(STATE_FILE)

            self.quizzes = quizzes
            self.best_score = best_score
            self.history = history
            best_text = "기록 없음" if best_score is None else f"{best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_text})")

        except FileNotFoundError:
            # 첫 실행: 아직 파일이 없음
            self.reset_to_default()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")

        except (json.JSONDecodeError, KeyError, TypeError, AttributeError, ValueError):
            # 파일 내용이 깨졌거나 형식이 맞지 않음 → 복구 절차
            ui.warn("데이터 파일이 손상되었습니다. 복구를 시작합니다.")
            self.recover_from_corruption()

        except OSError:
            # 권한 문제 등으로 파일을 읽을 수 없음
            ui.warn("데이터 파일을 읽을 수 없어 기본 퀴즈 데이터로 시작합니다.")
            self.reset_to_default()

    def find_valid_backups(self):
        """백업 파일 중 정상적으로 읽히는 것만 골라 (경로, 데이터) 목록으로 반환한다."""
        valid = []
        for path in self.backup.list_backups():
            try:
                valid.append((path, self.read_state(path)))
            except (OSError, json.JSONDecodeError, KeyError, TypeError, AttributeError, ValueError):
                continue  # 백업도 손상되었으면 목록에서 제외
        return valid

    def recover_from_corruption(self):
        """손상된 파일을 보관하고, 사용자가 고른 방법(백업 복원 / 기본 데이터)으로 복구한다."""
        # 1단계: 손상된 파일을 지우지 않고 따로 보관
        corrupted_path = self.backup.backup_corrupted()
        if corrupted_path is not None:
            ui.info(f"손상된 파일을 보관했습니다: backups/{os.path.basename(corrupted_path)}")

        # 2단계: 정상적으로 읽히는 백업 찾기
        valid_backups = self.find_valid_backups()

        # 3단계: 복구 방법 선택
        if not valid_backups:
            ui.warn("사용할 수 있는 백업이 없어 기본 퀴즈 데이터로 초기화합니다.")
            self.reset_to_default()
            method = "기본 데이터로 초기화 (사용 가능한 백업 없음)"
        else:
            print("\n🛟 복구 방법을 선택하세요.")
            print("  0. 기본 퀴즈 데이터로 초기화")
            for i, (path, (quizzes, best_score, _)) in enumerate(valid_backups, start=1):
                best_text = "기록 없음" if best_score is None else f"{best_score}점"
                print(f"  {i}. 백업 {os.path.basename(path)} (퀴즈 {len(quizzes)}개, 최고점수 {best_text})")
            choice = self.get_number("선택: ", 0, len(valid_backups))

            if choice == 0:
                self.reset_to_default()
                method = "기본 데이터로 초기화 (사용자 선택)"
            else:
                path, (quizzes, best_score, history) = valid_backups[choice - 1]
                self.quizzes = quizzes
                self.best_score = best_score
                self.history = history
                method = f"백업 {os.path.basename(path)}에서 복원 (사용자 선택)"

        # 4단계: 복구한 데이터를 저장 (손상 파일은 이미 보관했으므로 다시 백업하지 않음)
        self.save(make_backup=False)
        ui.success(f"복구 완료: {method}")

        # 5단계: 복구 로그 기록
        kept = os.path.basename(corrupted_path) if corrupted_path else "보관 실패"
        self.backup.write_log(f"손상 감지 → 손상 파일 보관({kept}) → {method}")

    def save(self, make_backup=True):
        """현재 퀴즈 목록, 최고 점수, 게임 기록을 state.json에 저장한다.
        make_backup이 True면 덮어쓰기 전에 기존 파일을 백업한다."""
        if make_backup:
            self.backup.create_backup()
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            ui.warn("데이터를 저장하지 못했습니다. (파일 쓰기 오류)")
