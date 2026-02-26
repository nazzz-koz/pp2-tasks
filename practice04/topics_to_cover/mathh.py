#1 Built-in Math Functions
a = min(5, 10, 25)
b = max(5, 10, 25)
c = abs(-7.25)
d = pow(4, 3)
e = round(1.77)

print(a)
print(b)
print(c)
print(d)
print(e)

#2 math Module Functions
import math

a = math.sqrt(64)
b = math.ceil(1.4)
c = math.floor(1.4)
d = math.pi
e = math.e

angle_rad = math.pi / 6  
sine_value = math.sin(angle_rad)
cosine_value = math.cos(angle_rad)

print(a)
print(b)
print(c)
print(d)
print(e)
print(sine_value, cosine_value)

#3 random Module
import random
print(random.random())
print(random.randint(1, 6))

colors = ["red", "blue", "green", "yellow"]
random_color = random.choice(colors)
print(f"Randomly selected color: {random_color}")

deck = ["Ace", "King", "Queen", "Jack", "10"]
random.shuffle(deck)
print("Shuffled deck:", deck)