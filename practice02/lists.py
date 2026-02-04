#1
thislist = ["apple", "banana", "cherry", "apple", "cherry"]
thislist = list(("apple", "banana", "cherry", "apple", "cherry"))
print(thislist)
print(len(thislist))

#2
list1 = ["abc", 34, True, 40, "male"]
print(type(list1))

#3
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[1])
print(thislist[-1])
print(thislist[2:5])
print(thislist[:4])
print(thislist[2:])
print(thislist[-4:-1])

#4
thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

#5
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1] = "blackcurrant"
print(thislist)
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)
thislist[5:6] = ["blackcurrant", "watermelon"]
print(thislist)
thislist[1:3] = ["watermelon"]
print(thislist)

#6
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)

#7
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

#8
thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)
thistuple = ("kiwi", "orange")
thislist.extend(thistuple)
print(thislist)

#9
thislist = ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.remove("banana")
print(thislist)

#10
thislist = ["apple", "banana", "cherry"]
thislist.pop(1)
print(thislist)
thislist.pop()
print(thislist)

#11
thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist)
del thislist

#12
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)

#13
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)
for i in range(len(thislist)):
  print(thislist[i])

#14
thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

#15
thislist = ["apple", "banana", "cherry"]
[print(x) for x in thislist]

#16
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [x for x in fruits if "a" in x]
print(newlist)

#17
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
for x in fruits:
  if "a" in x:
    newlist.append(x)
print(newlist)

#18
newlist = [x if x != "banana" else "orange" for x in fruits]

#19
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist2 = [100, 50, 65, 82, 23]
thislist3 = ["banana", "Orange", "Kiwi", "cherry"]

thislist.sort()
thislist2.sort(reverse = True)
thislist2.reverse()
thislist3.sort(key = str.lower)
print(thislist, thislist2, thislist3)

#20
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
mylist1 = list(thislist)
mylist2 = thislist[:]
print(mylist, mylist1, mylist2)

#21
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list1.extend(list2)
list3 = list1 + list2
for x in list2:
  list1.append(x)

print(list3)
