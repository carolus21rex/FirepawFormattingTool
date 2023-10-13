import csv


def main(self):
    print(3)


def import_file(file, settings):
    data = []
    with open(file, 'r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def set_import():
    return [("CSV Files", "*.csv")]
