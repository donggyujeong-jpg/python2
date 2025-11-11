#개발자 클래스를 정의: id, name, skill

class Developer:
    def __init__(self, id, name, skill):
        self.id = id
        self.name = name
        self.skill = skill

    def __str__(self):
        return f"Developer(ID: {self.id}, Name: {self.name}, Skill: {self.skill})"
    #인스턴스 생성
dev1 = Developer(1, "Alice", "Python")
dev2 = Developer(2, "Bob", "JavaScript")    

#인스턴스 정보 출력
print(dev1)
print(dev2)