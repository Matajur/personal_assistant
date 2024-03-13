"""Test file"""

def outer(x):
    def inner(y):
        return x + y
    return inner


add_five = outer(5)
print(add_five(3))
print(add_five(10))

