import json

# Load JSON data from file
with open('book_data.json', 'r') as file:
    json_data = json.load(file)



# Now json_data is a Python object
print(json_data["1"])

