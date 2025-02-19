import json
from constants import constants_dict

# Load the existing constants from constants.json
with open('constants.json', 'r') as json_file:
    constants_json = json.load(json_file)

# List to store found constants
found_constants = []

# Update the constants.json with LaTeX representations based on value and unit comparison
for constant in constants_json:
    for key, value in constants_dict.items():
        if constant['value'] == value.value and constant['unit'] == value.unit:
            constant['latex'] = value.latex
            found_constants.append(constant)
            break

# Save the updated constants back to constants.json
with open('constants.json', 'w') as json_file:
    json.dump(constants_json, json_file, indent=4)

# Print the list of found constants
print("Found and updated constants:")
for const in found_constants:
    print(f"Constant: {const['constant']}, LaTeX: {const['latex']}")

print("Updated constants.json with LaTeX representations based on value and unit comparison.")