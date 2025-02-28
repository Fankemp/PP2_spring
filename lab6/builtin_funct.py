import math
import time
import functools

# 1
def multiply_list(numbers):
    return functools.reduce(lambda x, y: x * y, numbers)

# Ex:
print(multiply_list([1, 2, 3, 4]))  # 24


# 2
def count_case(s):
    upper = sum(1 for char in s if char.isupper())
    lower = sum(1 for char in s if char.islower())
    return {"Uppercase": upper, "Lowercase": lower}

# Ex:
print(count_case("Hello World!")) 


# 3
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

# Ex:
print(is_palindrome("Racecar"))  # True
print(is_palindrome("hello"))    # False


# 4
def delayed_sqrt(number, milliseconds):
    time.sleep(milliseconds / 1000) 
    result = math.sqrt(number)
    print(f"Square root of {number} after {milliseconds} milliseconds is {result}")

# Ex:
delayed_sqrt(25100, 2123)  # Выведет корень из 25100 через 2.123 секунды


# 5
def all_true(t):
    return all(t)

# Ex:
print(all_true((True, True, True)))  # True
print(all_true((True, False, True))) # False
