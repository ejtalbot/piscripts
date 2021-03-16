import asyncio
import websockets

from controller import Board, rainbow_snake_background_cycle
from utils.conversions import create_color_pattern_by_name

board = Board()

#snakes
rainbow_color_names = ["red", "orange_red", "yellow", "electric_green", "blue", "violet"]
rainbow_colors = create_color_pattern_by_name(rainbow_color_names)

#snakes
purple_pink_names = ["pink_orange", "magenta", "purple_pizzazz", "violet"]
purple_pink_colors = create_color_pattern_by_name(rainbow_color_names)


board.add_snake("rainbow", 0, rainbow_colors, board.count, lengthen_sequence_by=2, reverse=False)
board.add_snake("purple_pink", 0, purple_pink_colors, board.count, lengthen_sequence_by=3, reverse=False)
board.set_active_snake("rainbow")

async def lights(websocket, path):
	command = await websocket.recv()
	if command == "off":
		board.off_switch = True
	if command == "rainbow":
		print("rainbow")

	await websocket.send(f"processing command {command}")

start_server = websockets.serve(lights, "0.0.0.0", 8765)
asyncio.ensure_future(board.multicolor_snake(board.snakes["rainbow"], crawl_length=5))
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()

#TODO keep going based on command
