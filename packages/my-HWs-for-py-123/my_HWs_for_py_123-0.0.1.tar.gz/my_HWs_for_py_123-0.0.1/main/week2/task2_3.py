# Task2_3 - Working with 'csv' and 'json' structures
# Имеется файл cars.csv
# Используйте библиотеку csv что бы прочитать содержимое файла.
# Конвертируйте данные в формат json и сохраните в файл cars.json
# Примечания:
# •	используйте csv.DictReader
# •	используйте json.dump с параметром indent=2
# •	используйте контекстный менеджер with для создания файла

import csv
import json
import os


def csv_to_json_converter(csv_file_path, json_file_path):
    cvs_data = []
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_string = csv.DictReader(csv_file)
        for row in csv_string:
              cvs_data.append(row)

    if os.path.splitext(json_file_path)[1] == '':
        json_file_path += '.json'
    if os.path.splitext(json_file_path)[1] != '.json':
        print("Incorrect file extension, should be .json")
    else:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json_string = json.dumps(cvs_data, indent=2)
            json_file.write(json_string)


if __name__ == '__main__':
    csv_path = input("Enter csv file name: ")
    json_path = input("Enter json file name: ")
    csv_to_json_converter(os.path.abspath(csv_path), os.path.abspath(json_path))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
