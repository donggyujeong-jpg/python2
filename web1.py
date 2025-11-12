# web1.py
# 크롤링하는 코드 작성
from bs4 import BeautifulSoup

page = open("Chap09_test.html", "rt", encoding="utf-8").read()
#스프객첼를 생성
soup = BeautifulSoup(page, "html.parser")
#모든  a태그를 검색 하여 리스트로 반환
# print(soup.prettify())

# print(soup.find("p"))
# print(soup.find_all("a"))

# print(soup.find_all("p", atters= {"class":"outer-text"}))

#태그내부의 문자열
for tag in soup.find_all("p"):
    title = tag.text.strip()    
    title = title.replace("\n", " ")
    print(title)
