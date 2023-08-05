# Task 4.	Unix `find' on Python.
# По аналогии с Unix утилитой find, реализуйте модуль на Python для поиска файлов и директорий на файловой системе.
# Обратите внимание на скрипт find_util
# bash$ ./find_util /usr/ -name "*.pyc" -type f
# Где "*.pyc" есть паттерн имени файл(ов) в формате shell-pattern
# Примечания:
# •	используйте os.walk
# •	используйте os.path.join
# •	для проверки имени файла на соответствие паттерну используйте fnmatch.


#!/usr/bin/env python
import sys
import argparse
import os
import fnmatch


def find(folder, name=None, show_dirs=True, show_files=True):
    """
    :param folder: path to a system folder from where to start searching
    :param name: file/directory name pattern, allows using '*' and '?' symbols
    :param show_dirs: if True - include directories into search results
    :param show_files: if True - include files into search results
    """
    no_match_found = 1
    for root, dirs, files in os.walk(folder):
        if show_dirs:
            for dir_name in dirs:
                if name is None:
                    print(f'Directory: {os.path.join(root, dir_name)}')
                elif fnmatch.fnmatch(dir_name, name):
                    print(f'Directory: {os.path.join(root, dir_name)}')
                    no_match_found = 0
        if show_files:
            for file_name in files:
                if name is None:
                    print(f'File: {os.path.join(root, file_name)}')
                elif fnmatch.fnmatch(file_name, name):
                    print(f'File: {os.path.join(root, file_name)}')
                    no_match_found = 0

    if name and no_match_found:
        print("No file/directory found matched to \'name\' pattern")


def parse_cmd_args():

    path_help = "Path to a folder"
    name_help = "File name pattern. Allows using '*' and '?' symbols"
    type_help = "Where 'f' means search only files, 'd' means only directories"

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help=path_help)
    parser.add_argument('-name', nargs='?', default=None, help=name_help)
    parser.add_argument('-type', nargs='?', default=None, choices=['f', 'd'], help=type_help)

    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    cmd, _ = parser.parse_known_args()

    files, dirs = True, True
    if cmd.type == 'd':
        files = False
    if cmd.type == 'f':
        dirs = False
    return cmd.path, cmd.name, dirs, files


if __name__ == '__main__':
    args = parse_cmd_args()
    find(*args)
