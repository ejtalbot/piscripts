from typing import List, Tuple

class Snake:
	def __init__(self, start: int, pattern: List[Tuple[int,int,int]], board_length: int, reverse: bool = False):
		#pattern cant be more than loength of board
		self.start = start
		self.reverse = reverse
		self.pattern = reversed(pattern) if reverse else pattern
		self.board_length = board_length

	@property
	def end(self):
		if self.reverse:
			return (self.start + len(self.pattern)) % self.board_length
		else:
			return (self.start - len(self.pattern)) % self.board_length 

	def move(self, steps: int, backwards: bool = False):
		if backwards:
			self.start = (self.start - steps) % self.board_length
		else:
			self.start = (self.start + steps) % self.board_length

	def iteration(self, func):
		for position, pixel in enumerate(range(self.start, len(self.pattern + start))):
			func(position, pixel if pixel < self.count else (pixel + 1) % self.count)
