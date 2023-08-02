from error import NotEmptyCoordinateError
from enum import Enum
from game_mark import GameMark
from board import GameBoard, Coordinate
from io_controller import IOController
from cpu_logic import DumbCPULogic
from typing import Tuple, List
class PlayerType(Enum):
    USER = 1
    CPU = 2

class Player:
    def __init__(self, name, mark) -> None:
        self.name = name
        self.mark = mark
        self.order = None
        self.player_type = None

    def make_move(self, board: GameBoard) -> None:
        coordinate = self.get_mark_coordinate(board)
        if board.is_empty(coordinate.row, coordinate.column):
            board.set_mark(coordinate, self.get_mark)
        else:
            raise NotEmptyCoordinateError()

    def get_mark_coordinate(self, board) -> Tuple[int, int]:
        raise NotImplementedError()

    def get_opponent_mark(self) -> GameMark:
        game_marks = GameMark.get_game_marks()
        game_marks.remove(self.get_mark())
        return game_marks[0]

    def player_type(self) -> PlayerType:
        return self.player_type

    def get_name(self) -> str:
        return self.name

    def get_mark(self) -> GameMark:
        return self.mark

    def play_order(self) -> int:
        return self.order
    
    def is_first_player(self):
        # 1 or Stringというのは必ずメモリロケーションがあるため、イコールを使う。
        # #Noneがあるの場合のみ is / is notをつかう                
        if self.play_order() == 1:
            return True
        return False

class CPUPlayer(Player):
    def __init__(self, name, mark) -> None:
        super().__init__(name, mark)
        self.player_type = PlayerType.CPU
    
    def get_mark_coordinate(self, board: GameBoard) -> Coordinate:
        return DumbCPULogic(self).generate_move(board)

class UserPlayer(Player):
    def __init__(self, name, mark) -> None:
        super().__init__(name, mark)
        self.player_type = PlayerType.USER
    
    def get_mark_coordinate(self) -> Coordinate:
        return IOController.get_coordinate_input("Mark (row, column): ")
