// script.js — 간단한 JavaScript 예제
// DOM이 준비되면 초기화 함수 실행
document.addEventListener('DOMContentLoaded', function(){
  // 카운터
  const countEl = document.getElementById('count');
  let value = 0;
  document.getElementById('incr').addEventListener('click', ()=>{ value++; updateCount(); });
  document.getElementById('decr').addEventListener('click', ()=>{ value--; updateCount(); });
  function updateCount(){ countEl.textContent = value; }

  // 테마 변경 (body 배경)
  const themeBtn = document.getElementById('themeBtn');
  themeBtn.addEventListener('click', ()=>{
    document.body.style.background = (document.body.style.background === 'linear-gradient(90deg, #264653, #2a9d8f)')
      ? '' : 'linear-gradient(90deg, #264653, #2a9d8f)';
  });

  // 색상 입력으로 배경 변경
  document.getElementById('applyColor').addEventListener('click', ()=>{
    const col = document.getElementById('colorInput').value;
    document.body.style.background = col;
  });

  // 현재 날짜 보여주기
  document.getElementById('showDate').addEventListener('click', ()=>{
    const out = document.getElementById('dateOutput');
    const now = new Date();
    out.textContent = now.toLocaleString();
  });

  // 간단한 더하기 처리
  document.getElementById('sumBtn').addEventListener('click', ()=>{
    const a = Number(document.getElementById('a').value) || 0;
    const b = Number(document.getElementById('b').value) || 0;
    const sum = a + b;
    document.getElementById('sumOutput').textContent = `결과: ${sum}`;
  });

});
