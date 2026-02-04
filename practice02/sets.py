#1
thisset = {"apple", "banana", "cherry", False, True, 0}
print(thisset)

#2
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x)
print("banana" in thisset)

#3
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)

#4
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
thisset.discard("apple")
thisset.clear()
print(thisset)

#5
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
set3 = set1 | set2
set1.update(set2)
set3 = set1.intersection(set2)
set3 = set1 & set2
set1.intersection_update(set2)
set3 = set1.difference(set2)
set3 = set1 - set2
set1.difference_update(set2)
set3 = set1.symmetric_difference(set2)
set3 = set1 ^ set2
set1.symmetric_difference_update(set2)

print(set3)

#6
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))