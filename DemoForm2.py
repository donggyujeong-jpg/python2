# DemoForm2.py
#DemoForm2.ui : 화면, DemoForm.py : 로직단
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
# web2.py
from bs4 import BeautifulSoup
import urllib.request


#파일 로딩 : 파일명 변경
from_class = uic.loadUiType("DemoForm2.ui")[0]

#폼 클래스 정의 (부모: QMainWindow, from_class)
class DemoForm(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.label.setText("첫번째 PyQt코딩")

    #슬럿 메서드
    def firstClick(self):
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
        self.label.setText("크롤링 완료")
    def secondClick(self):
        self.label.setText("두번째 버튼 클릭")
    def thirdClick(self):
        self.label.setText("세번째 버튼 클릭")

#직접 모듈을 실행한 경우만 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    app.exec_()

