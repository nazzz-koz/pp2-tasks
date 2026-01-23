#Creating Variables and do casting
a = 4  
a = "Sally" #initial value has changed
print(type(a)) #shows data type
x, y, z = "good", "better", "the best" #let assign multiple values at the same time
x = y = z = "better" #assign one value to 3 vars

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0


#Variable name rules
myvar = "D" # var must start with a letter or underscore
my_var = "D" # var cannot be a part of the Python keyboard
_my_var = "D" # var can only contain alpha-numeric characters and underscores
MYVAR = "D" # var names are case-sensitive
myvar2 = "D" # var name cannot start with a number


#Unpack a collection
fruits = ["apple", "banana", "cherry"] #extract the values into variables
x, y, z = fruits
print(x)
print(y)
print(z)


#Output vars
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)
print(x + y + z) #str cannot be added to num


#global var
global s #would have the same value in any part of the code
s = "Hello!"