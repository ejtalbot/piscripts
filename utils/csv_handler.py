import csv

def read_to_dict_list(file_name: str):
	with open(file_name, newline='') as csvfile:
		 csv_dict_list = list(csv.DictReader(csvfile, quoting=csv.QUOTE_ALL))
	return csv_dict_list
