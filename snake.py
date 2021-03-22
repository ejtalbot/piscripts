from typing import List, Tuple

from utils.conversions import lengthen_sequence


class Snake:
    def __init__(
        self,
        start: int,
        pattern_base: List[Tuple[int, int, int]],
        board_length: int,
        lengthen_sequence_by: int = 1,
        reverse: bool = False,
    ):
        self.start = start
        self.pattern_base = pattern_base
        self.pattern = lengthen_sequence(self.pattern_base, lengthen_sequence_by)
        self.reverse = reverse
        if self.reverse:
            self.pattern.reverse()
        self.board_length = board_length
        self.counter = 0

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
        for position, pixel in enumerate(
            range(self.start, len(self.pattern) + self.start)
        ):
            func(
                self.pattern,
                position,
                pixel if pixel < self.board_length else pixel % self.board_length,
            )
