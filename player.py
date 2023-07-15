from enum import Enum
from game_mark import GameMark
from io_controller import IOController
from cpu_logic import CPUStrategy
from typing import Tuple, List
class PlayerType(Enum):
    USER = 1
    CPU = 2

class Player:
    def __init__(self, name, mark) -> None:
        self.name = name
        self.mark = mark
        self.play_order = None
        self.player_type = None

    def make_move(self, board) -> None:
        row, column = self.get_mark_position(board)
        if board.is_empty(row, column):
            board.set_mark(row, column, self.mark)
        else:
            raise ValueError("The position is already marked. Please choose an empty cell.")

    def get_mark_position(self, board) -> Tuple[int, int]:
        raise NotImplementedError()


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

    def get_play_order(self):
        return self.play_order

class CPUPlayer(Player):
    def __init__(self, name, mark) -> None:
        super().__init__(name, mark)
        self.player_type = PlayerType.CPU
    
    def get_mark_position(self, board) -> Tuple[int, int]:
        return CPUStrategy.generate_cpu_move(board, self.mark, self.get_opponent_mark())

class UserPlayer(Player):
    def __init__(self, name, mark) -> None:
        super().__init__(name, mark)
        self.player_type = PlayerType.USER
    
    
    def get_mark_position(self, board) -> Tuple[int, int]:
        return IOController.get_position_input(board, "Mark (row, column): ")
