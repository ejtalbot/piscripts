import asyncio

import websockets

from controller import Board

board = Board()

"""
# snakes
rainbow_color_names = [
    "red",
    "orange_red",
    "yellow",
    "electric_green",
    "blue",
    "violet",
]
rainbow_colors = create_color_pattern_by_name(rainbow_color_names)

# snakes
purple_pink_names = ["pink_orange", "magenta", "purple_pizzazz", "violet"]
purple_pink_colors = create_color_pattern_by_name(purple_pink_names)

hot_names = ["red", "persian_red", "orange_red", "selective_yellow"]
hot_colors = create_color_pattern_by_name(hot_names)

cool_names = ["aquamarine", "teal", "blue", "violet"]
cool_colors = create_color_pattern_by_name(cool_names)


board.add_snake("rainbow", rainbow_colors, lengthen_sequence_by=12, reverse=False)
board.add_snake(
    "purple_pink", purple_pink_colors, lengthen_sequence_by=3, reverse=False
)
board.add_snake("cool", cool_colors, lengthen_sequence_by=4, reverse=False)
board.add_snake("hot", hot_colors, lengthen_sequence_by=8, reverse=False)
"""
board.set_active_snake("rainbow")
board.set_action("subset_color_wheel")


class LightSocket:
    def __init__(self, host: str, port: int, board: Board):
        self.host = host
        self.port = port
        self.run_server = websockets.serve(self.lights, self.host, self.port)
        self.board = board
        self.loop = asyncio.get_event_loop()

        self.start()

    def start(self):
        asyncio.ensure_future(self.board.execute_current_action())
        self.loop.run_until_complete(self.run_server)
        self.loop.run_forever()

    async def lights(self, websocket, path):
        command = await websocket.recv()
        await websocket.send(f"processing command {command}")
        if command == "off":
            board.off_switch = True
        if command in ["rainbow", "purple_pink", "hot", "cool"]:
            board.set_active_snake(command)
        if command in [
            "double_length",
            "reset_length",
            "half_length",
            "increase_pattern",
        ]:
            board.change_snake_length(command)
        if command in [
            "subset_color_wheel",
            "multicolor_snake",
            "blink_pattern",
            "fader",
            "random_walk",
            "randblink",
            "oneline",
            "rand_one_by_one",
            "mid_meet",
            "end_to_end",
        ]:
            board.set_action(command)
        if command == "stop":
            self.loop.stop()
            self.board.turn_off_all_pixels()


LightSocket("0.0.0.0", 8765, board)

# start_server = websockets.serve(lights, "0.0.0.0", 8765)
# asyncio.ensure_future(board.multicolor_snake(crawl_length=5))
# asyncio.ensure_future(board.execute_current_action())
# loop = asyncio.get_event_loop()
# loop.run_until_complete(start_server)
# loop.run_forever()

# TODO keep going based on command
