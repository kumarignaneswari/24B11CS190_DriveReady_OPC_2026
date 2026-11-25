
# TOPIC 06: DICTS AND JSON


MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}

# Access dictionary values
print(MENU["plum cake"])

# Safe dictionary lookup
print(MENU.get("donut", "not on menu"))

# Accessing a missing key causes KeyError
# MENU["donut"]

# Creating an order dictionary
order = {
    "name": "Ravi",
    "item": "plum cake",
    "qty": 2,
    "eggless": True
}

# Calculate total price
print(order["qty"] * MENU[order["item"]])

# Dictionary to JSON and JSON to dictionary
import json

text = json.dumps(order)
back = json.loads(text)

print(text)
print(back)


# TOPIC 07: FUNCTIONS, TYPE HINTS AND DOCSTRINGS

MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}


def get_price(item: str, qty: int = 1) -> int:
    """Return the total price in rupees for qty of an item on the Sweet Crumbs menu."""

    return MENU[item.lower().strip()] * qty


print(get_price("cupcake", 6))
print(get_price("Plum Cake"))


# TOPIC 08: DECORATORS

import functools


def log_call(func):
    # Takes a function as an argument

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Display function name and arguments
        print(f"Calling {func.__name__}{args}")

        # Execute the original function
        result = func(*args, **kwargs)

        # Display the returned result
        print(f"{func.__name__} returned {result!r}")

        return result

    return wrapper


# Apply decorator to get_price()
# Same as: get_price = log_call(get_price)

@log_call
def get_price(item: str, qty: int = 1) -> int:
    """Return the total price in rupees for qty of an item on the menu."""

    return MENU[item.lower().strip()] * qty


# Function calls
print(get_price("cupcake", 6))
print()

print(get_price("plum cake", 2))
print()

print(get_price("chocolate cake", 3))
print()

print(get_price("cupcake", 10))

# TOPIC 09: TRY / EXCEPT

import json

MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}


# Example 1: Handling ValueError

print("Example 1: Quantity")

try:
    qty = int(input("Enter quantity: "))
    print("Quantity:", qty)

except ValueError:
    print("Please enter a valid number.")

print()


# Example 2: Handling KeyError

print("Example 2: Menu lookup")

item = input("Enter cake name: ").lower().strip()

try:
    price = MENU[item]
    print("Price:", price)

except KeyError:
    print("Sorry, this item is not available on our menu.")

print()


# Example 3: Handling JSONDecodeError

print("Example 3: JSON parsing")

reply = '{"name": "Ravi", "item": "plum cake"}'

try:
    order = json.loads(reply)
    print("Customer:", order["name"])
    print("Item:", order["item"])

except json.JSONDecodeError:
    print("Invalid JSON format.")

print()
# Example 4: Multiple except blocks

print("Example 4: Multiple errors")

try:
    number = int(input("Enter a number: "))
    result = 100 / number
    print("Result:", result)

except ValueError:
    print("Please enter a valid number.")

except ZeroDivisionError:
    print("You cannot divide by zero.")

print()

print("Program completed successfully!")

