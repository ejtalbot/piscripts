import board
import neopixel
import random
import time

from utils.csv_handler import read_to_dict_list  


class Board:
	def __init__(self, gpio: str = "D18", count: int = 60):
		self.gpio = gpio
		self.count = count
		self.pixels = neopixel.NeoPixel(board.__getattribute__(gpio), self.count, brightness=.2, auto_write=False)

	def set_pixel_color(self, pixel_number: int, red: int, green: int, blue: int):
		print(red, green, blue)
		print(type({red, green, blue}))
		if any(not(0<=color<=255) for color in {red, green, blue}):
			print(f"invalid color outside rgb range: ({red, green, blue})")
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

	def cycle(self, red: int, green: int, blue: int):
		for pixel_number in range(self.count):
			self.set_pixel_color(pixel_number, red, green, blue)
			self.pixels.show()
			time.sleep(.1)

	def offset_light(self, offset: int, start: int, red: int, green: int, blue: int):
		for pixel_number in range(self.count):
			if (pixel_number + start) % offset == 0:
				self.set_pixel_color(pixel_number, red, green, blue)
		self.pixels.show()
		time.sleep(.5)

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
		# go to pixel 0, set it to first in color_dict_list
		# move to pixel 1
		# got to pixel 0 set to current color_dict_list
		# go to pixel 1, set to next colormin color_dict_list
		# go back to pixel 0
		color_dict_list = read_to_dict_list("resources/colors.csv")
		color_tuples = [tuple(color['rgb'].split(",")) for color in color_dict_list]
		for color in color_tuples:
			for pixel_number in reversed(range(1, self.count)):
				# get the previous pixel = self.pixels[pixel_number - 1]
				red, green, blue = self.get_pixel_rgb(pixel_number)
				print(red, green, blue)
				self.set_pixel_color(pixel_number -1, red, green, blue)
			print(color)
			print(type(color))
			self.set_pixel_color(0, color[0], color[1], color[2])
				# usee conversion
				#self.set_pixel_color(pixel_number, r, g, b)



board = Board()
board.full_color_wheel()
board.turn_off_all_pixels()
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
for i in range(10):
	board.offset_light(3, i, 255, 0, 255)
	board.offset_light(3, i+1, 255, 255, 0)
	board.offset_light(3, i+2, 0, 255, 255)
"""
board.turn_off_all_pixels()
