from quiz import Quiz


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
