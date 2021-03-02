import board
import neopixel
import random
import time

#TODO color scheme mapping rgb

COLORS = {
	"RED" = (255, 0, 0)
	"GREEN" = (0, 255, 0)
	"BLUE" = (0, 0, 255)
}

class Board:
	def __init__(self, gpio: str = "D18", count: int = 60):
		self.gpio = gpio
		self.count = count
		self.pixels = neopixel.NeoPixel(board.__getattribute__(gpio), self.count)

	def set_pixel_color(self, red: int, green: int, blue: int):
		if any(not(0<=color<=255) for color in {red, green, blue}):
			print(f"invalid color outside rgb range: ({red, green, blue})")
		else:
			self.pixels[pix_num] = (red, green, blue)

	def turn_off_pixel(self, pixel_number: int):
		self.pixels[pixel_number] = (0, 0, 0)

	def turn_off_all_pixels(self):
		for pixel_number in self.count:
			self.turn_off_pixel(pixel_number)

	def cycle(self, red: int, green: int, blue: int):
		for pixel_number in self.count:
			self.set_pixel_color(red, green, blue)
			time.sleep(.1)
			self.turn_off_pixel(pixel_number)

board = Board()
board.cycle(255, 0, 0)
board.cycle(0, 255, 0)
board.cycle(0, 0, 255)
