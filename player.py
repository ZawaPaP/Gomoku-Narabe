from error import NotEmptyCoordinateError
from enum import Enum
from game_mark import GameMark
from board import GameBoard, Coordinate
from io_controller import IOController
from cpu_logic import DumbCPULogic, HighCPULogic, CPULogic
from typing import Tuple, List, Type
class PlayerType(Enum):
    USER = 1
    CPU = 2

class Player:
    def __init__(self, name, mark) -> None:
        self.name = name
        self._mark = mark
        self.order = None
        self.opponent = None

    @property
    def mark(self) -> GameMark:
        return self._mark

    def make_move(self, board: GameBoard) -> None:
        coordinate = self.get_mark_coordinate(board)
        if board.is_coordinate_empty(coordinate):
            board.set_mark(coordinate, self.get_mark)
        else:
            raise NotEmptyCoordinateError()

    def set_opponent(self, opponent: 'Player'):
        self.opponent = opponent

    def get_mark_coordinate(self, board) -> Coordinate:
        raise NotImplementedError()

    def opponent_mark(self) -> GameMark:
        game_marks = GameMark.get_game_marks()
        game_marks.remove(self.mark)
        return game_marks[0]

    def get_name(self) -> str:
        return self.name

    def play_order(self) -> int:
        return self.order
    
    def is_first_player(self):             
        return self.play_order() == 1

class CPUPlayer(Player):
    def __init__(self, name, mark, logic: Type[CPULogic] = HighCPULogic) -> None:
        super().__init__(name, mark)
        self.player_type = PlayerType.CPU
        self.logic = logic(self)
    
    def get_mark_coordinate(self, board: GameBoard) -> Coordinate:
        return self.logic.generate_move(board)

class UserPlayer(Player):
    def __init__(self, name, mark) -> None:
        super().__init__(name, mark)
        self.player_type = PlayerType.USER
    
    def get_mark_coordinate(self, board) -> Coordinate:
        return IOController.get_coordinate_input(board, "Mark (row, column): ")
