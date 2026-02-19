#1
x = lambda a, b : a * b
print(x(5, 6))

#2
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))

#3
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

#4
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#5
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)