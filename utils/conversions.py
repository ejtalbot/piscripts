from typing import Tuple

def rgb_tuple_split(rgb_tuple: Tuple[str, str, str]):
	return int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2])

def create_rgb_tuple(red: int, green: int, blue: int):
	return tuple(red, green, blue)