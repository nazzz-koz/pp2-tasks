#1 
# Parent class
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

x = Person("John", "Doe")
x.printname()

#Child class
class Student(Person):
  pass

#execute the method
x = Student("Mike", "Olsen")
x.printname()

#2
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.
    Person.__init__(self, fname, lname)

x = Student("Mike", "Olsen")
x.printname()