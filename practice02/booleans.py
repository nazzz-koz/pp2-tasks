#1
print(10 > 9)
print(10 == 9)

#2
a = 22
b = 9
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#3
print(bool("Hello"))
print(bool(15))

#4
x = "Hello"
print(bool(x))

#5
print(bool(""))
print(bool(0))
print(bool(()))
print(bool(None))

#6
class myclass():
  def __len__(self):
    return 0
myobj = myclass()
print(bool(myobj))

#7
def myFunction() :
  return True
print(myFunction())

#8
def myFunction() :
  return True
if myFunction():
  print("YES!")
else:
  print("NO!")

#9
x = 200
print(isinstance(x, int))