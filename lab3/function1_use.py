from function1 import Grams_ounces, solve, filter_prime, reverse_sentence, is_palindrome

# граммов в унции
print("100 grams is equal to", Grams_ounces(100), "ounces")

# куры и кролики
chickens, rabbits = solve(35, 94)
print(f"There are {chickens} chickens and {rabbits} rabbits on the farm.")

# фильтрации простых чисел
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 19]
print("Prime numbers:", filter_prime(numbers))

#  переворот слов в предложении
sentence = "We are ready"
print("Reversed sentence:", reverse_sentence(sentence))

# Проверяем палиндромом
word = "racecar"
print(f"Is '{word}' a palindrome? {is_palindrome(word)}")
