#1 Convert from JSON to Python
import json
x =  '{ "name":"John", "age":30, "city":"New York"}'

y = json.loads(x)

print(y["age"])


#2 Convert from Python to JSON
import json
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

y = json.dumps(x)

print(y)


#3 Format the Result
import json

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(x, indent=4))
print(json.dumps(x, indent=4, separators=(". ", " = ")))
print(json.dumps(x, indent=4, sort_keys=True))


#4 Writing JSON Files
import json

data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "is_student": False,
    "courses": ["Math", "Science", "History"]
}

filename = 'data.json'

try:
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4) 
    print(f"Successfully wrote data to {filename}")
except IOError as e:
    print(f"Error writing to file: {e}")


#5 Reading JSON Files
import json

try:
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    print(data)
    print(f"Type of data: {type(data)}")

    print(f"Name: {data['name']}")
    print(f"Courses: {data['courses']}")

except FileNotFoundError:
    print("Error: The file 'data.json' was not found.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON: {e}")
