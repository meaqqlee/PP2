class MyClass:
  x = 5
  
p1 = MyClass()
print(p1.x)

User
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("John", 36)
print(p1.name)
print(p1.age)
#self is link for exemplire, __init__ defined as method in the class person

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name},{self.age}"
p1 = Person("Jhon", 36)
print(p1)

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def myfunc(self):
    print("Hello my name is " + self.name)
p1 = Person("John", 36)
p1.myfunc()

del p1.age

del p1

class Person:
  pass