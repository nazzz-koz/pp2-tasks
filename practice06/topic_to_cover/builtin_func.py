#1
nums = [1, 2, 3, 4]
print(len(nums))

#2
nums = [1, 2, 3]
print(sum(nums))

#3
nums = [5, 2, 9, 1]
print(min(nums))   
print(max(nums))   

#4
nums = [1, 2, 3]
squared = map(lambda x: x**2, nums)
print(list(squared))

#5
nums = [1, 2, 3, 4]
evens = filter(lambda x: x % 2 == 0, nums)
print(list(evens))

#6
from functools import reduce
nums = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, nums)
print(product)   

#7
fruits = ["apple", "banana"]
for i, fruit in enumerate(fruits):
    print(i, fruit)

#8
names = ["A", "B"]
scores = [90, 80]
zipped = zip(names, scores)
print(list(zipped))

#9
nums = [3, 1, 2]
print(sorted(nums))          
print(sorted(nums, reverse=True))  

words = ["apple", "kiwi", "banana"]
print(sorted(words, key=len))

#10
int("10")        
float("3.14")    
str(100)         

list("abc")      
tuple([1, 2])    
set([1, 1, 2])   

#11
bool(0)      
bool(1)      
bool("")     
bool("hi")   


#example
from functools import reduce
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x % 2 == 0, squares))
result = sum(evens)

print(result)