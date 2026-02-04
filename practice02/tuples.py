#1
tuple1 = ("abc", 34, True, 40, "male")
tuple1 = tuple(("abc", 34, True, 40, "male"))
print(tuple1)
print(len(tuple1))

#2
thistuple = ("apple",)
print(type(thistuple))

#3
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[1])
print(thistuple[-1])
print(thistuple[2:5])
print(thistuple[:4])
print(thistuple[2:])
print(thistuple[-4:-1])
if "apple" in thistuple:
  print("Yes, 'apple' is in the fruits tuple")

#4
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)
print(x)

#5
thistuple = ("apple", "banana", "cherry")

y = list(thistuple)
y.append("orange")
thistuple = tuple(y)

y = ("orange",)
thistuple += y
print(thistuple)

#6
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y)
del thistuple
print(thistuple)

#7
fruits = ("apple", "mango", "papaya", "pineapple", "cherry")
(green, *tropic, red) = fruits
print(green)
print(tropic)
print(red)

#8
thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x)
for i in range(len(thistuple)):
  print(thistuple[i])

#9
thistuple = ("apple", "banana", "cherry")
i = 0
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1

#10
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)
tuple3 = tuple1 + tuple2
print(tuple3)

fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2
print(mytuple)