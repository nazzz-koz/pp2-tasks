#Match Object

#1 basic search()
import re
#The search() function returns a Match object:
txt = "The rain in Spain"
x = re.search("ai", txt)
print(x)

#2 span()
import re
#Search for an upper case "S" character in the beginning of a word, and print its position:
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())

#3 string()
import re
#The string property returns the search string:
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)

#4 group
import re
#Search for an upper case "S" character in the beginning of a word, and print the word:
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())