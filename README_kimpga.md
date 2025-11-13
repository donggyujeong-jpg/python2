# kimpga_top20 사용법

이 폴더에는 `kimpga.com`에서 상위 코인 정보를 가져오는 간단한 스크래퍼가 포함되어 있습니다.

파일
- `kimpga_top20.py` - 메인 스크립트
- `requirements.txt` - 필요 패키지

설치 (PowerShell)

```powershell
python -m pip install -r .\requirements.txt
```

사용 예시

```powershell
# 기본: 상위 20개 크롤링
python .\kimpga_top20.py

# 상위 10개만
python .\kimpga_top20.py --top 10 --out-json top10.json --out-csv top10.csv
```

출력
- JSON: 기본 `kimpga_top.json`
- CSV: 기본 `kimpga_top.csv`

주의사항
- 웹사이트 구조(HTML)가 변경되면 파싱 실패 가능성이 있습니다. 이 경우 `kimpga_top20.py` 내의 파싱 함수를 조정해야 합니다.
- 사이트의 robots.txt와 이용 약관을 확인하고 과도한 요청을 보내지 마세요.
