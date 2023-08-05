import re
from socket import inet_aton


def check_ip(ip_address):
    try:
        inet_aton(ip_address)
    except (OSError, TypeError):
        return False
    return True

def check_ip_re(ip_address):
    try:
        is_ip_template = bool(re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ip_address))
        if is_ip_template:
            for item in ip_address.split('.'):
                if int(item) > 225:
                    return False
        else:
            return False
    except TypeError:
        return False
    return True


if __name__ == '__main__':
    assert check_ip('') is False
    assert check_ip('192.168.0.1') is True
    assert check_ip('0.0.0.1') is True
    assert check_ip('10.100.500.32') is False
    assert check_ip(700) is False
    assert check_ip('127.0.1') is True
