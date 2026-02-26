#1 Create a generator that generates the squares of numbers up to some number N.
def square_generator(N):
    i = 1
    while i * i <= N:
        yield i * i
        i += 1
N = int(input("N:"))
for square in square_generator(N):
    print(square)

#2 Write a program using generator to print the even numbers
# between 0 and n in comma separated form where n is input from console.
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
n = int(input("n:"))
print(",".join(str(num) for num in even_numbers(n)))

#3 Define a function with a generator which can iterate the numbers,
# which are divisible by 3 and 4, between a given range 0 and n.
def num(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 ==0:
            yield i
n = int(input("n:"))
for i in num(n):
    print(i)

#4 Implement a generator called squares to yield the square of all numbers from (a) to (b).
# Test it with a "for" loop and print each of the yielded values.

def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2
a = int(input("a:"))
b = int(input("b:"))
for square in squares(a, b):
    print(square)

#5 Implement a generator that returns all numbers from (n) down to 0.
def gen(n):
    while n>=0:
        yield n
        n -= 1
n = int(input("n:"))
for i in gen(n):
    print(i)