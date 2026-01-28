#1
print('Car is called "BMW"') 

#2
a = """A long text like this can be used as a variable too.
It is also a string."""
print(a)
print(type(a))

#3
b = "Lemon tree"
print(b[1]) 
print(b[::-1])

#4
for i in "diff": 
    print(i)

#5
c = "I am a student"
print(len(c)) 

#6
d = " Imagine having a looong text."
print("text" in d) 
print("text" not in d) 

#7
a = "  Welcome back!  " 
print(a.upper())
print(a.lower())
print(a.strip())
print(a.replace("!", "?"))
print(a.split("b"))

#8
age = 17
intro = f"My name is Jake, I am {age}" 
print(intro)

#9
ex = "We are the so-called \"Students\" from the south." 
print(ex)