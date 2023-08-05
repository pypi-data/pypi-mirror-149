import os
from prettytable import PrettyTable



def ls(file_path):
    res = PrettyTable()
    res.field_names = ["Mode", "Owner", "Group", "Size", "File name"]
    for item in os.listdir(file_path):
        info = os.stat(os.path.join(file_path, item))
        res.add_row([info.st_mode,
                     info.st_uid,
                     info.st_gid,
                     info.st_size,
                     item])
    print(res)

if __name__ == "__main__":
    ls("C:\\Users\\Denys_Voloshyn1\\Downloads\\HWs\\week2")
