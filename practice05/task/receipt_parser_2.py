#1 Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re
text = input("Enter string: ")
if re.fullmatch(r"ab*", text):
    print("Match found")
else:
    print("No match")

#2 Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
import re
text = input("Enter string: ")
if re.fullmatch(r"ab{2,3}", text):
    print("Match found")
else:
    print("No match")

#3 Write a Python program to find sequences of lowercase letters joined with a underscore.
import re
text = input("Enter text: ")
matches = re.findall(r"[a-z]+_[a-z]+", text)
print(matches)

#4 Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re
text = input("Enter text: ")
matches = re.findall(r"[A-Z][a-z]+", text)
print(matches)

#5 Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re
text = input("Enter string: ")
if re.fullmatch(r"a.*b", text):
    print("Match found")
else:
    print("No match")

#6 Write a Python program to replace all occurrences of space, comma, or dot with a colon.
import re
text = input("Enter text: ")
result = re.sub(r"[ ,\.]", ":", text)
print(result)

#7 Write a python program to convert snake case string to camel case string.
import re
text = input("Enter snake_case: ")
result = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)
print(result)

#8 Write a Python program to split a string at uppercase letters.
import re
text = input("Enter string: ")
result = re.split(r"(?=[A-Z])", text)
print(result)

#9 Write a Python program to insert spaces between words starting with capital letters.
import re
text = input("Enter string: ")
result = re.sub(r"([A-Z])", r" \1", text)
print(result.strip())

#10 Write a Python program to convert a given camel case string to snake case.
import re
text = input("Enter camelCase: ")
result = re.sub(r"([A-Z])", r"_\1", text).lower()
print(result)