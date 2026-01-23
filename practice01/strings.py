print('He is called "Johnny"') #quotes inside quotes

a = """A long text like this can be used as a variable too.
It is also a string."""
print(a)
print(type(a))

b = "Lemon tree"
print(b[1]) #slicing
print(b[::-1])

for i in "diff": #using loops
    print(i)

c = "I am a student"
print(len(c)) #length of a str

d = " Imagine having a looong text."
print("text" in d) 
print("text" not in d) #checks and outputs bool

a = "  Welcome back!  " #modify strings
print(a.upper())
print(a.lower())
print(a.strip())
print(a.replace("!", "?"))
print(a.split("b"))

age = 17
intro = f"My name is Jake, I am {age}" #f-string combination
print(intro)
num = 17.234567
txt = f"The price of a shirt is {num:.2f} dollars" 
txt2 = f"The pric efor that meal is {5*17} dollars"
print(txt)
print(txt2)

ex = "We are the so-called \"Students\" from the south." #Escape characters: \", \', \n, \r, \t, \b, \ooo, \hxx
print(ex)

#String methods
a = "zoRo"
print(a.capitalize())
print(a.casefold())
print(a.center(40))
print(a.count("o"))
print(a.encode())
print(a.endswith('a'))
print(a.expandtabs(2)) #works with \t
print(a.find('R'))
qwe = "Price is {wer:.2f} dollars!"
print(qwe.format(wer = 35))
print(a.index("z"))
print(a.isalnum()) #checks alphanumeric
print(a.isalpha()) #checks alphabet
print(a.isascii())
print(a.isdecimal())
print(a.isdigit())
print(a.isidentifier())
print(a.islower())
print(a.isnumeric())
print(a.isprintable())
print(a.isspace())
print(a.istitle())
print(a.isupper())
b = "-".join(a)
print(b)
print(a.ljust(10))
print(a.lower())
print(a.lstrip())
c = str.maketrans("R", "r")
print(a.translate(c))
print(a.partition("R"))
print(a.replace("R", "t"))
print(a.rfind("o"))
print(a.rindex("o"))
print(a.rjust(20))
print(a.rpartition('R'))
print(a.rsplit("o"))
print(a.rstrip())
print(a.split())
print(a.splitlines())
print(a.startswith('z'))
print(a.strip())
print(a.swapcase())
print(a.title())
print(a.upper())
print(a.zfill(10))