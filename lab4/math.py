import math


#task1
def degree_to_radian(degree):
    return round(degree * (math.pi / 180), 6)


#task2
def trapezoid_area(height, base1, base2):
    return 0.5 * (base1 + base2) * height

#task3
def regular_polygon_area(num_sides, side_length):
    return round((num_sides * (side_length ** 2)) / (4 * math.tan(math.pi / num_sides)), 2)

#task4
def parallelogram_area(base, height):
    return base * height



#Example:

#Ex: task1
degree = 15
print(f"Input degree: {degree}")
print(f"Output radian: {degree_to_radian(degree)}\n")

#Ex: task2
height = 5
base1 = 5
base2 = 6
print(f"Height: {height}")
print(f"Base, first value: {base1}")
print(f"Base, second value: {base2}")
print(f"Expected Output: {trapezoid_area(height, base1, base2)}\n")

#Ex: task3
num_sides = 4
side_length = 25
print(f"Input number of sides: {num_sides}")
print(f"Input the length of a side: {side_length}")
print(f"The area of the polygon is: {regular_polygon_area(num_sides, side_length)}\n")

#Ex: task4
base = 5
height2 = 6
print(f"Length of base: {base}")
print(f"Height of parallelogram: {height2}")
print(f"Expected Output: {parallelogram_area(base, height2)}")


