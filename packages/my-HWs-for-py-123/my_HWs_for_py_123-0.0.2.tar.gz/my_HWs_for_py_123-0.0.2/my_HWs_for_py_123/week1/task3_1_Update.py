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


def read_file():
    file = open('text.txt', "r", encoding='utf-8')
    string = file.read().lower()
    file.close()
    return string


def count_common_letter(str_chars):
    chars = dict()
    for i in str_chars:
        if i.isalpha():
            chars.update({i: str_chars.count(i)})
    return max(chars, key=chars.get)


def count_word_python(str_chars):
    words_list = str_chars.split()
    count = 0
    for x in words_list:
        if x == "python":
            count += 1
    return count


if __name__ == '__main__':
    my_file = read_file()
    assert count_common_letter(my_file) == 'e'
    assert count_word_python(my_file) == 6

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
