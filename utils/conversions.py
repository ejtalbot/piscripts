from typing import List, Tuple

def rgb_tuple_split(rgb_tuple: Tuple[str, str, str]):
	return int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2])

def create_rgb_tuple(red: int, green: int, blue: int):
	return tuple(red, green, blue)

def lengthen_sequence(sequence: List[str], multiplier: int):
	return [
		sub_item for sub_items in [[item]*multiplier for item in sequence] for sub_item in sub_items
	]
