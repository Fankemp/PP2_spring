#Task1
def square_generator(N):
    for i in range(N + 1):
        yield i ** 2



#Task2
def even_numbers_generator(N):
    for i in range(0, N + 1, 2):
        yield i


#Task3
def divisible_by_3_and_4(N):
    for i in range(N + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


#Task4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2


#task5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1