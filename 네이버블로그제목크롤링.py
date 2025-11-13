import requests
from bs4 import BeautifulSoup
import time

# 네이버 검색 URL
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%95%84%EC%9D%B4%ED%8F%B017&ackey=fc7jjjh6"

# 사용자 에이전트 설정 (필수)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Referer': 'https://www.naver.com'
}

try:
    # URL에 요청 보내기
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    
    # 상태 코드 확인
    if response.status_code == 200:
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 블로그 제목 찾기 (HTML 구조 분석)
        # 제목은 class='fds-comps-right-image-text-title' 인 a 태그에 있음
        blog_titles = soup.find_all('a', class_='fds-comps-right-image-text-title')
        
        if blog_titles:
            print(f"총 {len(blog_titles)}개의 블로그 글을 찾았습니다.\n")
            print("=" * 90)
            
            for idx, title_tag in enumerate(blog_titles, 1):
                # 제목 텍스트 추출 (mark 태그 포함)
                title_text = title_tag.get_text(strip=True)
                # 링크
                blog_link = title_tag.get('href')
                
                print(f"{idx}. {title_text}")
                print(f"   링크: {blog_link}")
                print("-" * 90)
        else:
            print("블로그 글 제목을 찾을 수 없습니다.")
            print("\n다른 선택자 시도 중...")
            
            # 대체 선택자 시도
            alternative_titles = soup.find_all('span', class_='fds-comps-text')
            if alternative_titles:
                print(f"대체 선택자로 {len(alternative_titles)}개 요소를 찾았습니다.")
                
    else:
        print(f"요청 실패. 상태 코드: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"요청 중 오류 발생: {e}")
except Exception as e:
    print(f"오류 발생: {e}")
