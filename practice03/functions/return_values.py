#1
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

#2
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

#3
def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)

#4
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)