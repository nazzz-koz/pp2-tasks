#1 generator function
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)

#2 Generators: yield keyword
def fun():
    yield 1            
    yield 2            
    yield 3            
 
for val in fun(): 
    print(val)

#3 Generator expressions
sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)

#4 Iterators: iter() and next()
s = "GFG"
it = iter(s)

print(next(it))
print(next(it))
print(next(it))

#5 Creating a custom iterator
class EvenNumbers:
    def __iter__(self):
        self.n = 2  
        return self

    def __next__(self):
        x = self.n
        self.n += 2  
        return x

even = EvenNumbers()
it = iter(even)

print(next(it))  
print(next(it)) 
print(next(it))  
print(next(it)) 
print(next(it))

#6 StopIteration exception
li = [100, 200, 300]
it = iter(li)

while True:
    try:
        print(next(it))
    except StopIteration:
        print("End of iteration")
        break