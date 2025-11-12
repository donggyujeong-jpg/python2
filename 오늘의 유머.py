# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
#파일 저장
f = open("todayhumor.txt", "wt", encoding="utf-8"   )

for n in range(1,11):
    #오늘의 유머 주소 
    data ='https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=' + str(n)
    print(data)
    #웹브라우져 헤더 추가 
    req = urllib.request.Request(data, \
                                headers = hdr)
    data = urllib.request.urlopen(req).read()
    page = data.decode('utf-8', 'ignore')
    soup = BeautifulSoup(page, 'html.parser')
    list = soup.find_all('td', attrs={'class':'subject'})

    for item in list:
            try:
                #<a class='list_subject'><span>text</span><span>text</span>
                # span = item.contents[1]
                # span2 = span.nextSibling.nextSibling
                title = item.find('a').text.strip()
                #속성을 검색할 경우
                href = item.find('a')['href']
                if re.search('일본', title):
                #정규식으로 '아이폰' 문자열이 있는지 검색
                    print(title)
                    print('https://www.todayhumor.co.kr + href')
                    f.write(title + "\n")
            except:
                pass
f.close()
        #<td class="subject">
#<a href="/board/view.php?table=bestofbest&amp;no=481166&amp;s_no=481166&amp;page=1" target="_top">한국 아마추어 러닝씬에 홀연히 등장한 노력의 천재</a>