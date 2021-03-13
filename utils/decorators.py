import asyncio
from functools import wraps

def interrupt(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		board_object = args[0]
		if board_object.off_switch:
			print("board switched off")
			board_object.turn_off_all_pixels()
		else:
			try:
				while not board_object.off_switch:
					await func(*args, **kwargs)
				print(f"broken out {board_object.off_switch}")
			except KeyboardInterrupt:
				print("Process interrupted")
	return wrapper