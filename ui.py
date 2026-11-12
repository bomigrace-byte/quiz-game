"""터미널 화면 꾸미기 도구 (표준 라이브러리만 사용)"""
import os
import sys

os.system("")  # Windows 터미널에서 색상 코드가 동작하도록 켜기

USE_COLOR = sys.stdout.isatty()  # 화면이 아닌 파일로 출력할 때는 색상 끄기

# ANSI 색상 코드: 터미널에 "글자색을 바꿔라"라고 보내는 특수 문자열
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"

WIDTH = 44  # 구분선 길이


def color(text, *codes):
    """글자에 색을 입혀서 반환한다."""
    if not USE_COLOR:
        return text
    return "".join(codes) + text + RESET


def line(char="─"):
    """얇은 구분선을 출력한다."""
    print(color(char * WIDTH, DIM))


def title(text):
    """위아래 두꺼운 선이 있는 제목을 출력한다."""
    print(color("═" * WIDTH, CYAN))
    print(color(f"  {text}", BOLD, CYAN))
    print(color("═" * WIDTH, CYAN))


def success(msg):
    print(color(f"✅ {msg}", GREEN))


def error(msg):
    print(color(f"❌ {msg}", RED))


def warn(msg):
    print(color(f"⚠️  {msg}", YELLOW))


def info(msg):
    print(color(f"💡 {msg}", BLUE))


def progress(current, total, size=20):
    """[■■■■□□□□] 3/8 형태의 진행률 막대를 출력한다."""
    filled = int(size * current / total)
    bar = "■" * filled + "□" * (size - filled)
    print(color(f"[{bar}] {current}/{total}", CYAN))


def score_message(score):
    """점수에 따라 다른 응원 문구를 반환한다."""
    if score == 100:
        return "🏆 완벽해요! 만점입니다!"
    elif score >= 80:
        return "🎉 훌륭해요!"
    elif score >= 50:
        return "👍 좋아요, 조금만 더!"
    else:
        return "📚 다시 도전해서 복습해 볼까요?"
