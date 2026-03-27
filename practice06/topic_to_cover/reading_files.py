#1
f = open("demofile.txt")
print(f.read())
f.close()

with open("demofile.txt") as f:
  print(f.read())

#2
with open("demofile.txt") as f:
  print(f.read(5))

#3
with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())

#4
with open("demofile.txt") as f:
  for x in f:
    print(x)

#5
with open("example.txt", "r") as file:
    lines = file.readlines() #returns lines as a list of strings
    for line in lines:
        print(line.strip())