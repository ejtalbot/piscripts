from typing import List, Tuple

from utils.conversions import lengthen_sequence

class Snake:
	def __init__(self, start: int, pattern: List[Tuple[int,int,int]], board_length: int, lengthen_sequence_by: int = 1, reverse: bool = False):
		#pattern cant be more than loength of board
		self.start = start
		self.pattern = lengthen_sequence(pattern, lengthen_sequence_by)
		self.reverse = reverse
		if self.reverse:
			self.pattern.reverse()
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
		for position, pixel in enumerate(range(self.start, len(self.pattern) + self.start)):
			func(self.pattern, position, pixel if pixel < self.board_length else (pixel) % self.board_length)
