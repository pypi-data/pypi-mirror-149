# 5.	Unix 'ls -lh' on Python.
# По аналогии с командой ls -lh для Unix систем, реализуйте модуль на Python который отображает содержимое директории
#
# Примечания:
# •	Чтобы получить содержимое директории используйте os.listdir
# •	Используйте os.stat чтобы получить информацию о каждом файле
# •	Используйте библиотеку prettytable
# 1.	pip install prettytable
# 2.	Имена столбцов: Mode, Owner, Group, Size, File name
# •	Используйте библиотеки pwd и grp чтобы получить имя пользователя и группу


import os
from prettytable import PrettyTable


def ls_lh(folder):
    files_table = PrettyTable(["Mode", "Owner", "Group", "Size", "File name"])
    files_table.align["File name"] = 'l'
    files_table.align["Size"] = 'r'
    files_counter = 0

    if not os.path.exists(folder):
        return print("No directory found with specified name")
    for filename in os.listdir(folder):
        stat_info = os.stat(os.path.join(folder, filename))
        if os.path.isdir(os.path.join(folder, filename)):
            filename = "\033[32m " + filename + " \033[0;0m"
        files_table.add_row(
            [stat_info.st_mode, stat_info.st_uid, stat_info.st_gid, file_size_converter(stat_info.st_size), filename])
        files_counter += 1
    if files_counter > 0:
        print(files_table.get_string(title="Folder " + folder))
    else:
        print("Specified folder is empty")


def file_size_converter(byte_size):
    units_array = ["B", "KB", "MB", "GB", "TB"]
    for i in units_array:
        if (byte_size // 1024 == 0) or (i == "TB"):
            return f"{round(float(byte_size), 1)}{i}"
        byte_size /= 1024


if __name__ == '__main__':
    dir_path = input("Enter dir name: ")
    ls_lh(os.path.abspath(dir_path))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
