# Like - 5

# Задание2 - 2.	Find min. and max. value.
# Имеется список:
# numbers = [1, 2, '0', '300', -2.5, 'Dog', True, 0o1256, None]
# Преобразуйте элементы списка в тип int(). Найдите минимальное и максимальное значение.

def print_min_max():
    numbers = [1, 2, '0', '300', -2.5, 'Dog', True, 0o1256, None]
    rez = []
    for item in numbers:
        try:
            rez.append(int(item))
        except (ValueError, TypeError):
            print(f'The value can\'t be converted to \'int\': {str(item)}')

    print(f'Result int array: {rez}')
    print(f'Max value: {max(rez)}')
    print(f'Min value: {min(rez)}')


if __name__ == '__main__':
    print_min_max()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
