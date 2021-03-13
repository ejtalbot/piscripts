import asyncio
import websockets

from controller import Board, rainbow_snake_background_cycle
from snake import Snake
from utils.conversions import create_color_pattern_by_name

board = Board()
rainbow_color_names = ["red", "orange_red", "yellow", "electric_green", "blue", "violet"]	
rainbow_colors = create_color_pattern_by_name(rainbow_color_names)
snake = Snake(0, rainbow_colors, board.count, lengthen_sequence_by=2, reverse=True)	

keep_going = True

async def lights(websocket, path):
    command = await websocket.recv()
    await websocket.send(f"command {command}")
    if command == "off":
    	board.off_switch = True
    	print(board.off_switch)
    else:
    	print("command")
    	print(board.off_switch)

start_server = websockets.serve(lights, "0.0.0.0", 8765)
asyncio.ensure_future(board.multicolor_snake(snake, crawl_length=5))
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()