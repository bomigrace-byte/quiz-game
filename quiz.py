import ui


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)
        self.hint = hint          # 힌트 (str, 없으면 빈 문자열)

    def display(self, number):
        """문제와 선택지를 화면에 출력한다."""
        print(ui.color(f"\n[문제 {number}]", ui.BOLD, ui.CYAN))
        print(ui.color(self.question, ui.BOLD))
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 반환한다."""
        return user_answer == self.answer

    def has_hint(self):
        """힌트가 있으면 True를 반환한다."""
        return self.hint != ""

    def to_dict(self):
        """JSON으로 저장할 수 있도록 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json에서 읽은 딕셔너리로 Quiz 객체를 만든다.
        형식이 잘못되었으면 ValueError를 발생시킨다."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        hint = data.get("hint", "")  # 예전 파일에는 hint가 없을 수 있다

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 사이의 번호여야 합니다.")
        if not isinstance(hint, str):
            raise ValueError("힌트 형식이 잘못되었습니다.")

        return cls(question, choices, answer, hint)
