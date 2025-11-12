from bs4 import BeautifulSoup
import urllib.request
#클리앙의 사용기 게시판 
response = urllib.request.urlopen('https://www.clien.net/service/board/use')
page = response.read().decode('utf-8', 'ignore')
soup = BeautifulSoup(page, 'html5lib')
list = soup.findAll('a', attrs={'class':'list_subject'})

for item in list:
        try: 
                #<a class='list_subject'><span>전자기기</span><span>제목</span></a>
                span = item.contents[3]
                title = span.text.strip()
                print(title)
        except:
                pass 
