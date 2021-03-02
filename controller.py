import board
import neopixel
import random
import time

#TODO color scheme mapping rgb

COLORS = {
	"RED": (255, 0, 0),
	"GREEN": (0, 255, 0),
	"BLUE": (0, 0, 255)
}

class Board:
	def __init__(self, gpio: str = "D18", count: int = 60):
		self.gpio = gpio
		self.count = count
		self.pixels = neopixel.NeoPixel(board.__getattribute__(gpio), self.count, brightness=.5, auto_write=False)

	def set_pixel_color(self, pixel_number: int, red: int, green: int, blue: int):
		if any(not(0<=color<=255) for color in {red, green, blue}):
			print(f"invalid color outside rgb range: ({red, green, blue})")
		else:
			self.pixels[pixel_number] = (red, green, blue)

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


board = Board()
#board.cycle(255, 0, 0)
#board.cycle(0, 255, 0)
#board.cycle(0, 0, 255)
for i in range(10):
	board.offset_light(3, i, 255, 0, 0)
	board.offset_light(3, i+1, 0, 255, 0)
	board.offset_light(3, i+2, 0, 0, 255)
board.turn_off_all_pixels()
