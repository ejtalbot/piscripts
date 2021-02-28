import board
import neopixel
import random
import time
pixels = neopixel.NeoPixel(board.D18, 30)
max_pixel = 60
blinks = 5

def rand_rbg():
	red = random.randint(0, 254)
	green = random.randint(0, 254)
	blue = random.randint(0, 254)
	return tuple((red, green, blue))

for pix_num in range(max_pixel):
	for blink in range(blinks):
		pixels[pix_num] = rand_rbg()
		time.sleep(.25)

for pix_num in reversed(range(max_pixel)):
	time.sleep(.1)
	pixels[pix_num] = (0, 0, 0)