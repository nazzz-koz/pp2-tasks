#1
x = 15
y = 4
print(x + y)
print(x - y)
print(x * y)
print(x / y) 
print(x % y)
print(x ** y)
print(x // y)

#2
print(x := 3)
x = 2
x **= 3
print(x)
x %= 3
print(x)

#3
numbers = [1, 2, 3, 4, 5]
if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

#4
x = 8
y = 9
print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

#5
x = 7
print(1 < x < 10)
print(1 < x and x < 10)

#6
x = 5
print(x > 0 and x < 10)
print(x < 5 or x > 10)
print(not(x > 3 and x < 10))

#7
x = ["apple", "tree"]
y = ["apple", "tree"]
z = x
print(x is z)
print(x is y)
print(x == y)
print(x is not y)


#8
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)
print("pineapple" not in fruits)

#9
print(6 & 3)
print(6 | 3)
print(6 ^ 3)

#10
print((6 + 3) - (6 + 3))
print(100 + 5 * 3)