import asyncio
import websockets

from controller import Board, rainbow_snake_background_cycle

board = Board()

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
asyncio.ensure_future(board.blink(255, 0, 0))
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()