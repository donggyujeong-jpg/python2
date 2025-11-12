# web2.py
from bs4 import BeautifulSoup
import urllib.request

#파일 저장
f = open("clien.txt", "wt", encoding="utf-8"   )

#10개의 글 크롤링
for i in range(0,10):

    url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)
    print(url)

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")   

    #검색
    list = soup.find_all("span", attrs={"data-role": "list-title-text"})   
    for tag in list:
        title = tag.text.strip()    
        print(title)        
        f.write(title + "\n")

f.close()

