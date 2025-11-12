# 웹 기초 연습 페이지 (HTML5 · CSS3 · JavaScript)

이 폴더는 간단히 HTML/CSS/JS를 학습하기 위한 예제 페이지를 포함합니다.

목록:
- `index.html` — 메인 페이지 (예제와 상호작용 버튼 포함)
- `style.css` — 기본 스타일
- `script.js` — 간단한 DOM 상호작용 예제

실행 방법:
1. 파일 탐색기에서 `d:\work\web_study\index.html` 더블클릭으로 브라우저에서 열기.

또는 PowerShell에서(작업 폴더가 `d:\work`인 경우):

```powershell
# 기본 브라우저로 열기
Start-Process .\web_study\index.html

n# 또는 로컬 서버에서 제공(파일 경로 문제를 피하려면 추천):
# Python이 설치되어 있으면 아래를 실행한 뒤 브라우저에서 http://localhost:8000 열기
cd .\web_study; python -m http.server 8000
```

학습 팁:
- HTML: 구조와 시맨틱 태그를 먼저 익히세요.
- CSS: 선택자와 박스 모델, 레이아웃(flex, grid)을 연습하세요.
- JS: DOM 선택, 이벤트, 간단한 상태 관리(예: 카운터)를 직접 구현해보세요.

원하시면 이 예제에 더 많은 연습 문제(폼 검증, 로컬 스토리지, 간단한 할 일 앱 등)를 추가해드릴게요.