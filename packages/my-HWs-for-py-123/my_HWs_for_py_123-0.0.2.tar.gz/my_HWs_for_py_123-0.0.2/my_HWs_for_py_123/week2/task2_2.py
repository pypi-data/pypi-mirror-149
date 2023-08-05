# Task 2.IP validation.
# Напишите функцию для валидации IP-адреса.
# Пример:
# def check_ip(ip_address):
#     return True/False
# Напишите несколько вариантов решения:
# •	используя библиотеку re
# •	используя socket.inet_aton

import socket
import re


def check_ip(ip_address):
    if re.fullmatch(r"^((((\d{1,2})|([0-1]?\d\d?)|(2[0-4]\d)|(25[0-5]))\.){2,3}"
                    r"((\d{1,2})|([0-1]?\d\d?)|(2[0-4]\d)|(25[0-5])))$", str(ip_address)):
        return True
    else:
        return False


def check_ip2(ip_address):
    if len(str(ip_address).split(".")) < 3:
        return False
    try:
        socket.inet_aton(str(ip_address))
        return True
    except OSError:
        return False


if __name__ == '__main__':

    assert check_ip('') is False
    assert check_ip('192.168.0.1') is True
    assert check_ip('0.0.0.1') is True
    assert check_ip('10.100.500.32') is False
    assert check_ip(700) is False
    assert check_ip('127.127.0.0') is True

    assert check_ip2('') is False
    assert check_ip2('192.168.0.1') is True
    assert check_ip2('0.0.0.1') is True
    assert check_ip2('10.100.500.32') is False
    assert check_ip2(700) is False
    assert check_ip2('127.0.1') is True

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
