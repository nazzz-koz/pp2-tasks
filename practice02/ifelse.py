#1
number = 15
if number > 0:
    print("The number is positive")
elif number < 0:
    priint("The number is negative")
else:
    print("The number is zero")

#2
if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")

#3
username = "Emil"
if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

#4
a = 5
b = 2
if a > b: print("a is greater than b")
print("A") if a > b else print("B")
bigger = a if a > b else b
print("Bigger is", bigger)
print("A") if a > b else print("=") if a == b else print("B")

#5
a = 200
b = 33
c = 500
if a > b and c > a:
  print("Both conditions are True")
if a > b or a > c:
  print("At least one of the conditions is True")
if not a > b:
  print("a is NOT greater than b")

#6
age = 25
has_license = True

if age >= 18:
  if has_license:
    print("You can drive")
  else:
    print("You need a license")
else:
  print("You are too young to drive")

#7
a = 33
b = 200
if b > a:
  pass