import re

#Task1
def abstr(string):
    pattern = r"ab*"
    match = re.fullmatch(pattern, string)
    return bool(match)

#Example:
print(abstr("a"))       # True
print(abstr("ab"))      # True
print(abstr("abb"))     # True
print(abstr("b"))       # False
print(abstr("abc"))     # False

#Task2
def abb(string):
    pattern = r"ab{2,3}$"
    match = re.fullmatch(pattern, string)
    return bool(match)

#Example:
print(abb("abb"))       # True
print(abb("abbb"))      # True
print(abb("a"))         # False
print(abb("ab"))        # False
print(abb("abbbb"))     # False

#Task3
def seqlow(string):
    pattern = r"[a-z]+_[a-z]+"
    lowe = re.findall(pattern, string)
    return lowe

#Example:
print(seqlow("abc_def"))       # ['abc_def']
print(seqlow("a_b"))           # ['a_b']
print(seqlow("abc_def_ghi"))   # ['abc_def', 'def_ghi']
print(seqlow("a1_b2"))         # []
print(seqlow("abcDef"))        # []

#Task4
def uplow(string):
    pattern = r"[A-Z][a-z]+"
    uplow = re.findall(pattern, string)
    return uplow


#Example:
print(uplow("Hello"))          # ['Hello']
print(uplow("HelloWorld"))     # ['Hello', 'World']
print(uplow("helloWorld"))     # ['World']
print(uplow("HELLOworld"))     # ['world']
print(uplow("AaaBbb"))         # ['Aaa', 'Bbb']



#task5
def a_b(string):
    pattern = r"a.*b$"
    match = re.fullmatch(pattern, string)
    return bool(match)


#Example:
print(a_b("ab"))        # True
print(a_b("acb"))       # True
print(a_b("a123b"))     # True
print(a_b("aXb"))       # True
print(a_b("b"))         # False
print(a_b("abX"))       # False





#Task6
def rep(string):
    return re.sub(r"[ ,.]", ":", string)


# Exmaple:
print(rep("hello world, this is a test."))   # "hello:world::this:is:a:test:"
print(rep("no,spaces.or,commas"))           # "no:spaces:or:commas"

#Task7
def snake_camel(string):
    word = string.split("_")
    camel = word[0] + "".join(w.capitalize() for w in word[1:])
    return camel

# Exmaple:
print(snake_camel("snake_case_example"))    # "snakeCaseExample"
print(snake_camel("longer_snake_case_string")) # "longerSnakeCaseString"


#Task8
def spli(string):
    return re.split(r"(?=[A-Z])", string)[1:]

# Exmaple:
print(spli("CamelCaseString"))  # ['', 'Camel', 'Case', 'String']
print(spli("AnotherExampleString"))  # ['', 'Another', 'Example', 'String']

#Task9
def ins(string):
    result = re.split(r"(?=[A-Z])", string)[1:]
    result2 = " ".join(result)
    return result2

# Exmaple:
print(ins("CamelCaseString"))  # "Camel Case String"
print(ins("ThisIsATest"))      # "This Is A Test"

#Task10
def camel_snake(string):
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", string)
    return snake.lower()

# Exmaple:
print(camel_snake("CamelCaseString"))  # "camel_case_string"
print(camel_snake("AnotherExampleString"))  # "another_example_string"
