import random
print(random.random())


print( random.sample(range(1, 46), 6))

from os.path import *
import os

fileName =  "c:\\python310\\python.exe"
print( basename(fileName) )
print( abspath("python.exe") )  

if exists(fileName):
    print("파일 크기:", getsize(fileName))
else:
    print("파일이 존재하지 않습니다.")   

#운영 체제정보
print( os.name )
print( os.environ )
# print( os.system('notepad.exe') )
print( os.getcwd() )

import glob
# print( glob.glob("c:\\work\\*.py") )

#raw string
print(glob.glob(r"c:\work\*.py"))

