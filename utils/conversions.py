from typing import List, Tuple
import os

from .csv_handler import read_to_color_name_dict

def rgb_tuple_split(rgb_tuple: Tuple[str, str, str]):
	return int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2])

def create_rgb_tuple(red: int, green: int, blue: int):
	return tuple(red, green, blue)

def lengthen_sequence(sequence: List[str], multiplier: int):
	return [
		sub_item for sub_items in [[item]*multiplier for item in sequence] for sub_item in sub_items
	]

def create_color_pattern_by_name(color_names: List[str]) -> List[Tuple[str,str,str]]:
	"""Gte a color pattern based on names passed in list"""
	pattern_rgb_colors = list()
	color_name_dict = read_to_color_name_dict(
		os.path.join(
			os.path.abspath(
				os.path.dirname(
					'resources/colors.csv'
				)
			),
			"colors.csv"
		)
	)
	for color in color_names:
		print(color)
		pattern_rgb_colors.append(color_name_dict.get(color, (0,0,0)))
	return pattern_rgb_colors
