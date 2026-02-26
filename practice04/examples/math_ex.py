#1 Write a Python program to convert degree to radian.
import math
degree = float(input("Input degree: "))
def degree_to_radian(degree):
    return degree * (math.pi / 180)
radian = degree_to_radian(degree)
print(f"Output radian: {radian:.6f}")

#2 Write a Python program to calculate the area of a trapezoid.
import math
h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))
def area_trapezoid(a, b, h):
    yield abs(((a+b)*h)/2)
for i in area_trapezoid(a, b, h):
    print(f"Expected Output: {i}")

#3 Write a Python program to calculate the area of regular polygon.
import math
sides = int(input("Input number of sides: "))
length = int(input("Input the length of a side: "))
def polygon(sides, length):
    return int((sides * (length ** 2)) / (4 * math.tan(math.radians(180 / sides))))
area = polygon(sides, length)
print(f"The area of the polygon is: {area}")

#4 Write a Python program to calculate the area of a parallelogram.
length = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
def parallelogram(length, height):
    return length * height
area = parallelogram(length, height)
print(f"Expected Output: {area}")