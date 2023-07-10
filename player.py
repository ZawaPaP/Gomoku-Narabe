from enum import Enum
from game_mark import GameMark
from io_controller import IOController
from cpu_logic import CPUStrategy
from typing import Tuple, List
class PlayerType(Enum):
    USER = 1
    CPU = 2

class Player:
    def __init__(self, name, mark, player_type) -> None:
        self.name = name
        self.mark = mark
        self.player_type = player_type

    def make_move(self, board) -> None:
        row, column = self.get_mark_position(board)
        if board.is_empty(row, column):
            board.set_mark(row, column, self.mark)
        else:
            raise ValueError("The position is already marked. Please choose an empty cell.")
            

    def get_mark_position(self, board) -> Tuple[int, int]:
        if self.player_type == PlayerType.CPU:
            return CPUStrategy.generate_cpu_move(board, self.mark, self.get_opponent_mark())
        else:
            return IOController.get_position_input(board, "Mark 'row, column': ")

    def get_opponent_mark(self) -> List[str]:
        game_marks = GameMark.get_game_marks()
        game_marks.remove(self.get_mark())
        return game_marks

    def get_type(self):
        return self.player_type

    def get_name(self):
        return self.name

    def get_mark(self):
        return self.mark
