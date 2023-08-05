# Like 5
import time

# Task5 - Multiples of 3 and 5. Find the best algorithm.
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 100000000.
# source: https://projecteuler.net/problem=1

def timer(foo):
    def wrapper():
        start = time.time()
        foo()
        finish = time.time()
        print(f"The run time is - {finish - start}s")
    return wrapper


@timer
def print_sum_multiples():
    sum_multiples = 0
    range_value = 100000000

    for i in range(5, range_value, 5):
        sum_multiples += i

    for i in range(3, range_value, 3):
        if i % 5 == 0:
            pass  # Наверное, стоит переходить на след. итерацию?
        else:
            sum_multiples += i

    print(f'Sum of all the multiples of 3 or 5 below 100000000: {sum_multiples}')


if __name__ == '__main__':
    for i in range(10):
        print_sum_multiples()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
