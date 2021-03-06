import board
import neopixel
import random
import time
pixels = neopixel.NeoPixel(board.D18, 60)
max_pixel = 59
blinks = 5

def rand_rbg():
	red = random.randint(0, 255)
	green = random.randint(0, 255)
	blue = random.randint(0, 255)
	return tuple((red, green, blue))

for pix_num in range(max_pixel):
	for blink in range(blinks):
		pixels[pix_num] = rand_rbg()
		time.sleep(.2)

for pix_num in reversed(range(max_pixel)):
	time.sleep(.1)
	pixels[pix_num] = (0, 0, 0)