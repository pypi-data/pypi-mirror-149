# Задание1 - List filtering.
# Дан объект типа list():
# l = [1, 2, '3', 4, None, 10, 33, 'Python', -37.5]
# Релизуйте функцию которая отфильтрует только integer (int) значения из этого списка.
# Напишите несколько вариантов решения:
# •	используя цикл for
# •	используя list comprehensions
# •	используя filter() + lambda


def list_filtering_for(list_items):
    list_int = list()
    for x in list_items:
        if isinstance(x, int):
            list_int.append(x)
    return list_int


def list_filtering_lambda(list_items):
    list_int = list(filter(lambda x: isinstance(x, int), list_items))
    return list_int


def list_filtering_comprehensions(list_items):
    list_int = [x for x in list_items if isinstance(x, int)]
    return list_int


if __name__ == '__main__':
    assert list_filtering_lambda([1, 2, '3', 4, None, 10, 33, 'Python', -37.5]) == [1, 2, 4, 10, 33]
    assert list_filtering_lambda([1, 2, 'a', 'b']) == [1, 2]
    assert list_filtering_lambda([1, 'a', 'b', 0, 15]) == [1, 0, 15]
    assert list_filtering_lambda([1, 2, 'aasf', '1', '123', 123]) == [1, 2, 123]

    assert list_filtering_for([1, 2, '3', 4, None, 10, 33, 'Python', -37.5]) == [1, 2, 4, 10, 33]
    assert list_filtering_for([1, 2, 'a', 'b']) == [1, 2]
    assert list_filtering_for([1, 'a', 'b', 0, 15]) == [1, 0, 15]
    assert list_filtering_for([1, 2, 'aasf', '1', '123', 123]) == [1, 2, 123]

    assert list_filtering_comprehensions([1, 2, '3', 4, None, 10, 33, 'Python', -37.5]) == [1, 2, 4, 10, 33]
    assert list_filtering_comprehensions([1, 2, 'a', 'b']) == [1, 2]
    assert list_filtering_comprehensions([1, 'a', 'b', 0, 15]) == [1, 0, 15]
    assert list_filtering_comprehensions([1, 2, 'aasf', '1', '123', 123]) == [1, 2, 123]


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
