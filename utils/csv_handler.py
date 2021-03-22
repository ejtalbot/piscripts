import csv


def read_to_dict_list(file_name: str):
    with open(file_name, newline="") as csvfile:
        csv_dict_list = list(csv.DictReader(csvfile, quoting=csv.QUOTE_ALL))
    return csv_dict_list


def read_to_color_name_dict(file_name: str):
    with open(file_name, newline="") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
        color_dict = dict()
        for row in csv_dict_reader:
            color_dict[row["name"]] = tuple(row["rgb"].split(","))
    return color_dict
