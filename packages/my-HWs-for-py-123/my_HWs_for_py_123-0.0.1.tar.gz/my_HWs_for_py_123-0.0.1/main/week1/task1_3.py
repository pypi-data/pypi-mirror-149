# Like - 4

# Зфдание3 - Letters Count.
# Имеется текст:
#
# Python is an interpreted high-level programming language for general-purpose programming. Created by Guido van Rossum and first released in 1991, Python has a design philosophy that emphasizes code readability, notably using significant whitespace. It provides constructs that enable clear programming on both small and large scales. In July 2018, the creator Guido Rossum stepped down as the leader in the language community after 30 years.
# Python features a dynamic type system and automatic memory management. It supports multiple programming paradigms, including object-oriented, imperative, functional and procedural, and has a large and comprehensive standard library.
# Python interpreters are available for many operating systems. CPython, the reference implementation of Python, is open source software and has a community-based development model, as do nearly all of Python's other implementations. Python and CPython are managed by the non-profit Python Software Foundation. Привет из Харькова!
#
# Определите какая буква наиболее часто встречается в этом тексте и сколько раз в этом тексте встречается слово 'Python'?
#
# Примечания:
# •	не учитывайте регистр букв, т.е. 'A' = 'a'
# •	не учитывайте знаки препинания и спецсимволы (кавычки, тире)
# •	не учитывайте пробелы и переводы строк

def print_common_letter():
    chars = {}
    tmp = 0
    with open('text.txt', "r", encoding='utf-8') as file:
        string = file.read()

    for i in string.lower():
        if i.isalpha():
            chars.update({i: string.count(i)})
            tmp += 1

    print(f'Letter occurs more in the text: {max(chars, key=chars.get)}')
    print(f"First count of iterations {tmp}")
    # print(f'Word "Python" occurs {string.count("Python")} times')


def print_common_letter2():
    chars = {}
    tmp = 0
    with open('text.txt', "r", encoding='utf-8') as file:
        string = file.read()

    while True:
        if string == '':
            break
        i = string[0]
        if i.isalpha():
            chars.update({i: string.count(i)})
        string = string.replace(i, '')
        tmp += 1

    print(f'Letter occurs more in the text: {max(chars, key=chars.get)}')
    print(f"Second count of iterations {tmp}")



if __name__ == '__main__':
    print_common_letter()
    print_common_letter2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
