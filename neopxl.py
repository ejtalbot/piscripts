import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30)
max_pixel = 10

for pix_num in range(max_pixel):
	pixels[pix_num] = (255, 0, 0)
	time.sleep(.25)
	pixels[pix_num] = (0, 255, 0)
	time.sleep(.25)
	pixels[pix_num] = (0, 0, 255)
	time.sleep(.25)
	pixels[pix_num] = (0, 0, 0)
	time.sleep(.25)

for pix_num in reversed(range(max_pixel)):
	pixels[pix_num] = (255, 0, 0)
	time.sleep(.25)
	pixels[pix_num] = (0, 255, 0)
	time.sleep(.25)
	pixels[pix_num] = (0, 0, 255)
	time.sleep(.25)
	pixels[pix_num] = (0, 0, 0)
	time.sleep(.25)
