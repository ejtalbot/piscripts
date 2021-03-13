import asyncio
import websockets

from controller import rainbow_snake_background_cycle

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


async def lights(websocket, path):
	keep_running = True
    command = await websocket.recv()
    print(f"< {command}")
    print(f"< {type(command)}")
    rainbow_snake_background_cycle()

    await websocket.send(f"command {command}")

start_server = websockets.serve(lights, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()