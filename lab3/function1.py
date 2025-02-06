import random
from itertools import permutations

#TASK1
def Grams_ounces(grams):
    return 28.3495231 * grams

#TASK2

def fahrenheit_to_celsius(f):
    return (5 / 9) * (f - 32)

#TASK3
def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if 2 * chickens + 4 * rabbits == numlegs:
            return chickens, rabbits
    return None

#TASK4
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    return [num for num in numbers if is_prime(num)]

#TASK5
def string_permutations(s):
    return [''.join(p) for p in permutations(s)]


#TASK6
def reverse_sentence(sentence):
    return ' '.join(sentence.split()[::-1])


#TASK7
def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False


#TASK8
def spy_game(nums):
    code = [0, 0, 7]
    code_index = 0
    for num in nums:
        if num == code[code_index]:
            code_index += 1
        if code_index == len(code):
            return True
    return False

#TASK9
def sphere_volume(radius):
    return (4 / 3) * 3.141592653589793 * (radius ** 3)

#TASK10
def unique_elements(lst):
    unique_list = []
    for item in lst:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

#TASK11
def is_palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]

#TASK12
def histogram(lst):
    for num in lst:
        print('*' * num)

#TASK13
def guess_the_number():
    name = input("Hello! What is your name? ")
    number = random.randint(1, 20)
    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")
    guesses = 0

    while True:
        guess = int(input("Take a guess: "))
        guesses += 1

        if guess < number:
            print("Your guess is too low.")
        elif guess > number:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break