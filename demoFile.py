# demoFile.py
#쓰기
f = open("demo.txt", "wt", encoding="utf-8" )
f.write("첫번째\n두번째\n세번째\n")
f.close()

#읽기
f = open("demo.txt", "rt", encoding="utf-8" )
content = f.read()
print(content)
f.close()

#문자열 데이터 처리 메서드
data = "  spam, egg and ham"
result = data.strip()        #양쪽 공백 제거
print(data)
print(result)
result2 = result.replace("ham", "ham egg")  #문자열 바꾸기
print(result2)
lst = result2.split()
print(lst)
print( ":)".join(lst) )  #문자열 합치기

print(len("abcd"))  #문자열 길이
print("hello".upper())  #대문자 변환
print("HELLO".lower())  #소문자 변환
print("2580".isdecimal())


import re
result = re.match("[0-9]*th", "35th")
print(result)
print(result.group())

result = re.search("[0-9]*th", "35th")
print(result)
print(result.group())

#단어검색
result = re.search("apple","this is apple")
print(result.group())

result = re.search("\d{4}","올해는 2025년 입니다")
print(result.group())
print(result.group())

