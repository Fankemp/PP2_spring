#TASK 1
class StringMethod:
    string = ""

    def getString(self):
        StringMethod.string = input("Write a string:")
    def printString(self):
        print(StringMethod.string.upper())


#TASK 2

class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length
    def area(self):
        return self.length ** 2

#TASK 3

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.widthx
    

# TASK 4
import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"Point coordinates: ({self.x}, {self.y})")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

#TASK5

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print("Deposit: ", self.balance)
        
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdraw {amount}, New balance {self.balance}")
        else:
            print("Not enough money")

#TASK6

def Isprime(x):
    if x < 2:
        return False
    
    for i in range(2, int(x**0.5)+ 1):
        if x % i == 0:
            return False
    return True

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 ,15 ,16]
prime_numbers = list(filter(lambda x: Isprime(x), numbers))
print(prime_numbers)
