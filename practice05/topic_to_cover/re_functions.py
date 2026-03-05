#RegEx Functions

#1 findall()
import re
#Return a list containing every occurrence of "ai";
# The list contains the matches in the order they are found.
#If no matches are found, an empty list is returned
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

#2 search()
import re
#If no matches are found, the value None is returned
#If there is more than one match, only the first occurrence of the match will be returned
txt = "The rain in Spain"
x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start()) 

#3 split()
import re
#Split the string at the first white-space character
#1 in example represents 1st appearance
txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)

#4 sub()
import re
#Replace the first two occurrences of a white-space character with the digit 9
#2 in example represents replacement of the first 2 occurrences
txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)

