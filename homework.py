import csv, json, yaml
from pprint import pprint


# Задание 1
def write_csv(data, src="write.csv"):
    with open(src, "w") as file:
        reader = csv.writer(file)
        for row in data:
            reader.writerow(row)


def read_csv(src):
    with open(src) as file:
        reader = csv.DictReader(file)
        result = []
        for row in reader:
            result.append(row)
    return result


# Задание 2
def write_json(data, src="write.json"):
    with open(src, "w") as file:
        json.dump(data, file, indent=4)


def read_json(src):
    with open(src) as file:
        return json.load(file)


# Задание 3
def write_yml(data, src="write.yml"):
    with open(src, "w") as file:
        yaml.safe_dump(data, file)


def read_yml(src):
    with open(src) as file:
        return yaml.safe_load(file)


# Задание 4
def csv_to_json(csv_file_path,json_file_path ):
    arr = []

    with open(csv_file_path) as csvFile:
        csvReader = csv.DictReader(csvFile)
        print(csvReader)
        for csvRow in csvReader:
            arr.append(csvRow)

    with open(json_file_path, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent=4))


# Задание 6
def json_to_yaml(json_file_path):
    json = read_json(json_file_path)
    write_yml(json)

