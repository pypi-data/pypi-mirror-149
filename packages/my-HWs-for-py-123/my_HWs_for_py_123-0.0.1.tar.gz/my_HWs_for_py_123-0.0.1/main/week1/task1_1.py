# Like - 5

# Задание1 - FizzBuzz task.
# Напишите программу, которая выводит на экран числа от 1 до 100.
# При этом, если число кратно 3-м, вместо него программа должна вывести слово Fizz, а если кратно 5 — слово Buzz.
# Если число кратно и 3 и 5, то программа должна выводить слово FizzBuzz

def print_num():
    for i in range(1, 100):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


if __name__ == '__main__':
    print_num()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
