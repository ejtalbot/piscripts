import asyncio
import board
import neopixel
import random
import time
from typing import List, Tuple

from snake import Snake
from utils.conversions import rgb_tuple_split, lengthen_sequence, create_color_pattern_by_name, convert_strings_in_tuple_to_ints, modulo_position_in_count
from utils.csv_handler import read_to_dict_list, read_to_color_name_dict
from utils.decorators import interrupt


class Board:
	def __init__(self, gpio: str = "D18", count: int = 60):
		self.gpio = gpio
		self.count = count
		self.pixels = neopixel.NeoPixel(board.__getattribute__(gpio), self.count, brightness=.2, auto_write=False)
		self.off_switch = False

	def set_pixel_color(self, pixel_number: int, red: int, green: int, blue: int):
		if any(not(0<=color<=255) for color in {red, green, blue}):
			print(f"invalid color outside rgb range: ({red, green, blue})")
		elif self.off_switch:
			self.turn_off_all_pixels()
		else:
			self.pixels[pixel_number] = (red, green, blue)

	def get_pixel_color(self, pixel_number: int):
		return self.pixels[pixel_number]

	def get_pixel_rgb(self, pixel_number: int):
		return self.pixels[pixel_number][0], self.pixels[pixel_number][1], self.pixels[pixel_number][2]

	def turn_off_pixel(self, pixel_number: int):
		self.pixels[pixel_number] = (0, 0, 0)

	def turn_off_all_pixels(self):
		for pixel_number in range(self.count):
			self.turn_off_pixel(pixel_number)
		self.pixels.show()

	async def cycle(self, red: int, green: int, blue: int):
		while not self.off_switch:
			for pixel_number in range(self.count):
				self.set_pixel_color(pixel_number, red, green, blue)
				self.pixels.show()
				asyncio.sleep(.1)
		print("turn off all pixels")
		self.turn_off_all_pixels()

	@interrupt
	async def blink(self, red: int, green: int, blue: int):
		for pixel_number in range(self.count):
			self.set_pixel_color(pixel_number, red, green, blue)
			self.pixels.show()
			await asyncio.sleep(.1)
		self.turn_off_all_pixels()
		await asyncio.sleep(1)
		print("turned off all pixels")

	def offset_light(self, offset: int, start: int, red: int, green: int, blue: int):
		for pixel_number in range(start, self.max_step(start, self.count, offset), offset):
			self.set_pixel_color(pixel_number, red, green, blue)
		self.pixels.show()
		time.sleep(.5)

	@staticmethod
	def max_step(start: int, max_count: int, divisor: int):
		max_plus_start_quotient = (start + max_count) // divisor
		max_quotient = max_count // divisor
		step_adjustment = (max_plus_start_quotient - max_quotient) * divisor
		return start + max_count - step_adjustment

	def primary_color_fade(self, pixel_number: int, rgb: int):
		if rgb not in range(3):
			print(f"invalid {rgb}")
		else:
			current_pixel = self.pixels[pixel_number]
			red = current_pixel[0]
			green = current_pixel[1]
			blue = current_pixel[2]
			if rgb == 0:
				red = max(0, current_pixel[0]-51)
			elif rgb == 1:
				green = max(0, current_pixel[1]-51)
			else:
				blue = max(0, current_pixel[2]-51)
			self.set_pixel_color(pixel_number, red, green, blue)

	def fade_all_primary_to_black(self, rgb: int):
		while any(
			pixel for pixel in self.pixels if pixel[rgb] > 0
		):
			for pixel_number in range(self.count):
				self.primary_color_fade(pixel_number, rgb)
			self.pixels.show()
			time.sleep(.5)

	def primary_color_increase(self, pixel_number: int, rgb: int):
		if rgb not in range(3):
			print(f"invalid {rgb}")
		else:
			current_pixel = self.pixels[pixel_number]
			red = current_pixel[0]
			green = current_pixel[1]
			blue = current_pixel[2]
			if rgb == 0:
				red = min(255, current_pixel[0]+51)
			elif rgb == 1:
				green = min(255, current_pixel[1]+51)
			else:
				blue = min(255, current_pixel[2]+51)
			self.set_pixel_color(pixel_number, red, green, blue)

	def increase_all_primary(self, rgb: int):
		while any(
			pixel for pixel in self.pixels if pixel[rgb] < 255
		):
			for pixel_number in range(self.count):
				self.primary_color_increase(pixel_number, rgb)
			self.pixels.show()
			time.sleep(.5)

	def full_color_wheel(self):
		color_dict_list = read_to_dict_list("resources/colors.csv")
		color_tuples = [tuple(color['rgb'].split(",")) for color in color_dict_list]
		for color in color_tuples:
			for pixel_number in reversed(range(1, self.count)):
				red, green, blue = self.get_pixel_rgb(pixel_number-1)
				self.set_pixel_color(pixel_number, red, green, blue)
			red, green, blue = rgb_tuple_split(color)
			self.set_pixel_color(0, red, green, blue)
			self.pixels.show()
			time.sleep(.1)

	def subset_color_wheel(self, colors: List[Tuple[str, str, str]]):
		loop_count = 10
		for i in range(loop_count):
			for pixel_number in range(self.count):
				color_position = (pixel_number + i) % len(colors)
				red, green, blue = rgb_tuple_split(colors[color_position])
				self.set_pixel_color(pixel_number, red, green, blue)
			self.pixels.show()
			time.sleep(.1 + .1*(i % 3))

	def snake(self, color: Tuple[str, str, str], length: int):
		red, green, blue = rgb_tuple_split(color)
		loop_count = 80 # TODO make a while loop
		start = 0
		end = length
		for pixel in range(start, length + 1):
			self.set_pixel_color(pixel, red, green, blue)
		self.pixels.show()
		time.sleep(.1)
		dividend = self.count
		for i in range(loop_count):
			self.turn_off_pixel(start)
			start = (start + 1) % self.count
			end = ((end + 1) % self.count)
			self.set_pixel_color(end, red, green, blue)
			self.pixels.show()
			time.sleep(.1)

	def multicolor_snake(
		self,
		snake: Snake,
		crawl_length: int = 60,
	):
		for background_rgb in snake.pattern_base:
			# can comment if snake fills entire
			self.set_range_of_pixels(snake.start, snake.start + len(snake.pattern), rgb_tuple_split(background_rgb), inside = False)
			for i in range(crawl_length):
				background_red, background_green, background_blue = rgb_tuple_split(background_rgb)
				self.set_pixel_color(snake.start, background_red, background_green, background_blue)
				snake.move(1)
				snake.iteration(self.move_pattern)
				self.pixels.show()
				time.sleep(.5)

	def light_all_off_pixels(self, rgb: Tuple[int, int, int] = (255, 255, 255)):
		for pixel_number, pixel in enumerate(self.pixels):
			if pixel == [0, 0, 0]:
				self.set_pixel_color(pixel_number, rgb[0], rgb[1], rgb[2])

	def set_range_of_pixels(self, start: int, stop: int, color: Tuple[str, str, str], inside: bool = True):
		red, green, blue = rgb_tuple_split(color)
		if inside:
			for pixel_number in range(start, stop + 1):
				self.set_pixel_color(modulo_position_in_count(pixel_number, self.count), red, green, blue)
		else:
			for pixel_number in range(0, start):
				self.set_pixel_color(modulo_position_in_count(pixel_number, self.count), red, green, blue)
			for pixel_number in range(stop, self.count):
				self.set_pixel_color(modulo_position_in_count(pixel_number, self.count), red, green, blue)

	def move_pattern(self, pattern, position, pixel):
		current_pixel = pixel if pixel < self.count else (pixel + 1) % self.count
		red, green, blue = rgb_tuple_split(pattern[position])
		self.set_pixel_color(current_pixel, red, green, blue)

#snake lengths
#snake color - set range of
	def opposite_whirl(self, snake_1: List[Tuple[str, str, str]], snake_2: List[Tuple[str,str,str]]):
		#snake_1
		#snake_2
		#start snake1 at beginning
		snake_1_tail = 0
		snake_1_head = len(snake_1)
		#set lights in range for snake1
		#increment like ranbow
		#start snake2 at end
		snake_2_tail = self.count - 1
		snake_2_head = snake_2_tail - len(snake_2)
		#set lights in range for snake2
		#


def rainbow_snake_background_cycle():
	board = Board()
	rainbow_color_names = ["red", "orange_red", "yellow", "electric_green", "blue", "violet"]	
	rainbow_colors = create_color_pattern_by_name(rainbow_color_names)
	snake = Snake(0, rainbow_colors, board.count, lengthen_sequence_by=2, reverse=True)
	board.multicolor_snake(
		snake,
		crawl_length=20,
	)
	board.turn_off_all_pixels()

rainbow_snake_background_cycle()


#board = Board()

#board.subset_color_wheel([(255,0,127), (239,187,204), (235,76,66)])
#board.full_color_wheel()
#board.turn_off_all_pixels()
"""
board.increase_all_primary(0)
board.fade_all_primary_to_black(0)
board.increase_all_primary(1)
board.fade_all_primary_to_black(1)
board.increase_all_primary(2)
board.fade_all_primary_to_black(2)
board.cycle(255, 0, 255)
board.cycle(255, 255, 0)
board.cycle(0, 255, 255)

rainbow_colors = create_color_pattern_by_name(["red", "orange_color_wheel", "yellow", "electric_green", "blue", "violet"])

board.multicolor_snake(lengthen_sequence(rainbow_colors, 2))

for i in range(10):
	board.offset_light(3, i, 255, 0, 255)
	board.offset_light(3, i+1, 255, 255, 0)
	board.offset_light(3, i+2, 0, 255, 255)
"""
#board.turn_off_all_pixels()
