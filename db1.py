# db1.py
#영구적으로 파일에  저장c

import sqlite3
#이름 변경
con = sqlite3.connect(r"d:\work\sample.db")  # 메모리 DB에 연결
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS PhoneBook(name text, phoneNum text);")

cur.execute("INSERT INTO PhoneBook VALUES('홍길동', '010-1234-5678');")

name = '이순신'
phoneNum = '010-9876-5432'
cur.execute("INSERT INTO PhoneBook VALUES(?, ?);", (name, phoneNum))        

datalist = (('강감찬', '010-1111-2222'),
            ('김유신', '010-3333-4444'))
cur.executemany("INSERT INTO PhoneBook VALUES(?, ?);", datalist)

#검색
# for row in cur.execute("SELECT * FROM PhoneBook;"):
#     print(row)

# 패치메서드 호출
cur.executescript("SELECT * FROM PhoneBook; INSERT INTO PhoneBook VALUES('홍길동', '010-1234-5678');")
print("-- fetchone() ---")
print(cur.fetchone())

print("-- fetchmany(2) ---")
print(cur.fetchmany(2))

print("-- fetchall() ---")
cur.execute("SELECT * FROM PhoneBook;")
print(cur.fetchall())

#정상적으로 완료
con.commit()  # 변경사항 저장