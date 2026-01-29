import os
print("this is file named test.py")
print(__name__)
print(__file__)
print(os.path.dirname(__file__))
def add():
    return 10