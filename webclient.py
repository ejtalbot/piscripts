import asyncio

import websockets


async def send_message():
    uri = "ws://192.168.0.150:8765"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        command = input("Enter input")

        await websocket.send(command)
        print(f"> {command}")

        response = await websocket.recv()
        print(f"< {response}")


asyncio.get_event_loop().run_until_complete(send_message())
