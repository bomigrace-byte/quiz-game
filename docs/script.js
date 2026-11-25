// ===== 1. 실행 명령어 복사 버튼 =====
const copyButton = document.getElementById("copy-button");
copyButton.addEventListener("click", function () {
  const command = document.getElementById("run-command").textContent;
  navigator.clipboard.writeText(command);
  copyButton.textContent = "복사됨!";
  setTimeout(function () { copyButton.textContent = "복사"; }, 1500);
});

// ===== 2. 웹에서 맛보기 퀴즈 =====
// quiz_data.py의 기본 퀴즈 7개와 같은 내용
const quizzes = [
  { question: "Python에서 정수(숫자)를 나타내는 자료형은?", choices: ["str", "int", "bool", "list"], answer: 2, hint: "integer(정수)의 줄임말입니다." },
  { question: "Python에서 '키:값' 쌍으로 데이터를 저장하는 자료형은?", choices: ["list", "tuple", "dict", "str"], answer: 3, hint: "dictionary(사전)처럼 단어로 뜻을 찾는 구조입니다." },
  { question: "반복 횟수가 정해져 있지 않고, 조건이 참인 동안 계속 반복할 때 주로 쓰는 문법은?", choices: ["for", "if", "def", "while"], answer: 4, hint: "영어로 '~하는 동안'이라는 뜻입니다." },
  { question: "클래스에서 객체가 생성될 때 자동으로 실행되는 메서드는?", choices: ["__init__", "__str__", "__main__", "__call__"], answer: 1, hint: "initialize(초기화)의 줄임말입니다." },
  { question: "원격 저장소(GitHub)를 내 컴퓨터로 통째로 복제하는 Git 명령어는?", choices: ["git pull", "git push", "git clone", "git init"], answer: 3, hint: "복제 양 '돌리'를 떠올려 보세요." },
  { question: "새 브랜치를 만들면서 바로 그 브랜치로 이동하는 명령어는?", choices: ["git branch -d", "git checkout -b", "git merge", "git add -A"], answer: 2, hint: "'이동하다'라는 명령어에 branch의 b 옵션을 붙입니다." },
  { question: "원격 저장소의 최신 변경사항을 내 로컬 저장소로 가져와 합치는 명령어는?", choices: ["git pull", "git commit", "git log", "git status"], answer: 1, hint: "push(밀다)의 반대말입니다." },
];

const box = document.getElementById("quiz-box");
let order = [];       // 이번 판의 문제 순서
let current = 0;      // 지금 몇 번째 문제인지 (0부터)
let correct = 0;      // 맞힌 개수
let earned = 0;       // 획득 점수
let usedHint = false; // 이번 문제에서 힌트를 봤는지

// 문제 순서를 무작위로 섞는다 (Python의 random.sample과 같은 역할)
function shuffle(list) {
  const copy = list.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function startQuiz() {
  order = shuffle(quizzes);
  current = 0;
  correct = 0;
  earned = 0;
  showQuestion();
}

function showQuestion() {
  const quiz = order[current];
  usedHint = false;

  // 진행률 막대: ■■■□□□□
  const filled = "■".repeat(current + 1) + "□".repeat(order.length - current - 1);

  box.innerHTML = `
    <p class="progress">[${filled}] ${current + 1}/${order.length}</p>
    <p class="question">${quiz.question}</p>
    <div class="choices">
      ${quiz.choices.map((choice, i) => `<button data-number="${i + 1}">${i + 1}. ${choice}</button>`).join("")}
    </div>
    <button id="hint-button">💡 힌트 보기 (정답 시 절반 점수)</button>
    <p class="message" id="message"></p>
  `;

  box.querySelectorAll(".choices button").forEach(function (button) {
    button.addEventListener("click", function () {
      checkAnswer(Number(button.dataset.number));
    });
  });

  document.getElementById("hint-button").addEventListener("click", function () {
    usedHint = true;
    showMessage(`💡 힌트: ${quiz.hint}`, "hint");
  });
}

function showMessage(text, className) {
  const message = document.getElementById("message");
  message.textContent = text;
  message.className = "message " + className;
}

function checkAnswer(number) {
  const quiz = order[current];
  const perQuestion = 100 / order.length;

  // 버튼을 다시 누르지 못하게 막기
  box.querySelectorAll("button").forEach(function (button) { button.disabled = true; });

  if (number === quiz.answer) {
    correct += 1;
    earned += usedHint ? perQuestion / 2 : perQuestion;
    showMessage("✅ 정답입니다!", "correct");
  } else {
    showMessage(`❌ 오답입니다. 정답은 ${quiz.answer}번입니다.`, "wrong");
  }

  // 1.2초 뒤 다음 문제 또는 결과
  setTimeout(function () {
    current += 1;
    if (current < order.length) {
      showQuestion();
    } else {
      showResult();
    }
  }, 1200);
}

function showResult() {
  const score = Math.round(earned);
  box.innerHTML = `
    <p class="question">🏆 결과: ${order.length}문제 중 ${correct}문제 정답! (${score}점)</p>
    <p class="note">실제 게임에서는 점수가 state.json에 저장되고, 최고 점수와 기록을 확인할 수 있습니다.</p>
    <button id="restart-button">다시 풀기</button>
  `;
  document.getElementById("restart-button").addEventListener("click", startQuiz);
}

startQuiz();

// ===== 3. 학습 목표 모두 펼치기 / 접기 =====
const toggleGoals = document.getElementById("toggle-goals");
toggleGoals.addEventListener("click", function () {
  const items = document.querySelectorAll("#goals details");
  const shouldOpen = toggleGoals.textContent === "모두 펼치기";
  items.forEach(function (item) { item.open = shouldOpen; });
  toggleGoals.textContent = shouldOpen ? "모두 접기" : "모두 펼치기";
});

// ===== 학습 목표 슬라이드 넘기기 =====
const slides = [
      { src: "slides/01-cover.png", title: "표지: 퀴즈 게임 하나로 4가지 기초를 익힌다" },
      { src: "slides/02-map.png", title: "학습목표 지도: 4개 영역, 15개 목표" },
      { src: "slides/03-variable.png", title: "목표 1. 변수는 값에 붙이는 이름표" },
      { src: "slides/04-types.png", title: "목표 2. 자료형 5가지의 차이" },
      { src: "slides/05-flow.png", title: "목표 3–5. 조건, 반복, 함수" },
      { src: "slides/06-klass.png", title: "목표 6–8. 클래스와 객체" },
      { src: "slides/07-fileio.png", title: "목표 9–11. 파일 입출력과 state.json" },
      { src: "slides/08-git.png", title: "목표 12–13. Git 기본 흐름과 명령어 7종" },
      { src: "slides/09-branch.png", title: "목표 14–15. 브랜치, clone과 pull" },
      { src: "slides/10-mission.png", title: "정리: 목표는 미션 어디에서 확인되나" },
      { src: "slides/11-check.png", title: "셀프 체크: 15개 질문" },
];

let slideIndex = 0;
const slideImage = document.getElementById("slide-image");
const slideCount = document.getElementById("slide-count");
const slideCaption = document.getElementById("slide-caption");
const thumbButtons = document.querySelectorAll(".thumb");

function showSlide(index) {
  // 처음에서 이전, 마지막에서 다음을 누르면 반대쪽 끝으로 돌아간다
  slideIndex = (index + slides.length) % slides.length;
  const slide = slides[slideIndex];
  slideImage.src = slide.src;
  slideImage.alt = slide.title;
  slideCaption.innerHTML = "";
  slideCount.textContent = (slideIndex + 1) + " / " + slides.length;
  slideCaption.append(slideCount, " " + slide.title);
  thumbButtons.forEach(function (button, i) {
    button.classList.toggle("active", i === slideIndex);
  });
}

document.getElementById("slide-prev").addEventListener("click", function () { showSlide(slideIndex - 1); });
document.getElementById("slide-next").addEventListener("click", function () { showSlide(slideIndex + 1); });
thumbButtons.forEach(function (button) {
  button.addEventListener("click", function () { showSlide(Number(button.dataset.index)); });
});

// 슬라이드 영역이 화면에 보일 때만 키보드 ← → 로 넘긴다
document.addEventListener("keydown", function (event) {
  const box = document.getElementById("slides").getBoundingClientRect();
  const visible = box.top < window.innerHeight && box.bottom > 0;
  if (!visible) return;
  if (event.key === "ArrowLeft") showSlide(slideIndex - 1);
  if (event.key === "ArrowRight") showSlide(slideIndex + 1);
});

showSlide(0);
