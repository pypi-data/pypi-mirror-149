import csv
import json


def csv_to_json(file_in, file_out):
    with open(file_in, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_data = []
        with open(file_out, 'w') as json_file:
            for item in csv_reader:
                csv_data.append(item)
            json_file.write(json.dumps(csv_reader, indent=2))


if __name__ == '__main__':
    csv_to_json('cars.csv', 'cars.json')
