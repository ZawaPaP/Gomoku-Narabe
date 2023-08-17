from game_mark import GameMark
from error import OutRangeCoordinateError, NoOutCastMarkError, NoLineExistError
from typing import Tuple, List, Set
from collections import Counter
class BoardCell:
    def __init__(self) -> None:
        self.mark = GameMark.EMPTY.value

class Coordinate:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        
    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.row == other.row and self.column == other.column
        return False

    def __hash__(self):
        return hash((self.row, self.column))

class GameBoard:
    ROW = 9
    COLUMN = 9

    def __init__(self) -> None:
        self.board = [[BoardCell() for _ in range(self.column())] for _ in range(self.row())]
        # marked coordinates (1 ~ 9)

    @staticmethod
    def row() -> int:
        return GameBoard.ROW

    @staticmethod
    def column() -> int:
        return GameBoard.COLUMN

    def row_range(self) -> range:
        return range(1, self.row() + 1)

    def column_range(self) -> range:
        return range(1, self.column() + 1)

    def get_mark(self, row, column) -> GameMark:
        return self.board[row - 1][column - 1].mark
        
    # set mark on the coordinate
    def set_mark(self, coordinate: Coordinate, mark: GameMark) -> None:
        self.board[coordinate.row - 1][coordinate.column - 1].mark = mark

    # remove mark from the coordinate
    def remove_mark(self, coordinate: Coordinate):
        self.board[coordinate.row - 1][coordinate.column - 1].mark = GameMark.EMPTY.value

    def is_in_board(self, coordinate: Coordinate) -> bool:
        if coordinate.row in self.row_range() and coordinate.column in self.column_range():
            return True
        else:
            raise OutRangeCoordinateError()

    def is_empty(self) -> bool:
        for i in self.row_range():
            for j in self.column_range():
                if self.get_mark(i, j) != GameMark.EMPTY.value:
                    return False
        return True

    # check if the coordinate is empty or not
    def is_cell_empty(self, row, column) -> bool:
        return self.get_mark(row, column) == GameMark.EMPTY.value


    # check if the coordinate is empty or not
    def is_coordinate_empty(self, coordinate: Coordinate) -> bool:
        return self.get_mark(coordinate.row, coordinate.column) == GameMark.EMPTY.value
    
    # check if board is full or not and return bool
    def is_full(self) -> bool:
        for i in self.row_range():
            for j in self.column_range():
                if self.is_cell_empty(i, j):
                    return False
        return True

    # get horizontal, vertical, diagonals lines of the coordinate
    def get_lines_from_coordinate(self, coordinate: Coordinate) -> List['Line']:
        lines = [
            RowLine(self, coordinate),
            ColumnLine(self, coordinate),
            PrincipalDiagonalLine(self, coordinate),
            SecondaryDiagonalLine(self, coordinate)
        ]
        return lines

class Line:
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        self.board = board
        self.coordinate = coordinate
        self.start = self._start_index()
        self.end = self._end_index()
        self._line = self._generate_line()
        self._index = self._coordinate_index()

    def __eq__(self, other):
        if isinstance(other, Line):
            return (self.start, self.end) == (other.start, other.end)
        return False

    def __hash__(self):
        return hash((self.start, self.end))

    @property
    def line(self) -> List[GameMark]:
        raise NotImplementedError()
    
    def _start_index(self):
        raise NotImplementedError()

    def _end_index(self):
        raise NotImplementedError()
    
    def _coordinate_index(self):
        raise NotImplementedError()
    
    def _generate_line(self):
        raise NotImplementedError()

    def get_board_coordinate(self, list_index: int) -> Coordinate(int, int):
        raise NotImplementedError()

    def is_empty(self) -> bool:
        if self.line == None:
            raise NoLineExistError()
        return all(mark == GameMark.EMPTY.value for mark in self.line)

# list of marks from the coordinate - row direction
class RowLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        self.start = self._start_index()
        self.end = self._end_index()
        self._line = self._generate_line()
        self._index = self._coordinate_index()
        
    @property
    def line(self) -> List[GameMark]:
        return self._line

    @line.setter
    def line(self, value: List[GameMark]) -> None:
        self._line = value
        
    def _start_index(self):
        return (self.coordinate.row, 1)

    def _end_index(self):
        return (self.coordinate.row, 9)

    def _coordinate_index(self):
        return self.coordinate.column - 1

    def _generate_line(self):
        return [mark for mark in [self.board.get_mark(self.coordinate.row, column) for column in self.board.column_range()]]

    def get_board_coordinate(self, list_index: int) -> Coordinate(int, int):
        return Coordinate(self.coordinate.row, 1 + list_index)

# list of marks from the coordinate - column direction
class ColumnLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        self.start = self._start_index()
        self.end = self._end_index()
        self._line = self._generate_line()
        self._index = self._coordinate_index()
        
    @property
    def line(self) -> List[GameMark]:
        return self._line
    
    def _start_index(self):
        return (1, self.coordinate.column)

    def _end_index(self):
        return (9, self.coordinate.column)

    def _coordinate_index(self):
        return self.coordinate.row - 1

    def _generate_line(self):
        return [mark for mark in [self.board.get_mark(row, self.coordinate.column) for row in self.board.row_range()]]

    def get_board_coordinate(self, list_index: int) -> Coordinate(int, int):
        return Coordinate(1 + list_index, self.coordinate.column)

# list of marks from the coordinate - up left to down right direction
class PrincipalDiagonalLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate):
        super().__init__(board, coordinate)
        self.start = self._start_index()
        self.end = self._end_index()
        self._line = self._generate_line()
        self._index = self._coordinate_index()
        
    @property
    def line(self) -> List[GameMark]:
        return self._line

    def _start_index(self) -> Tuple[int, int]:
        _distance_to_start_edge = min(self.coordinate.row, self.coordinate.column) - 1
        return (self.coordinate.row - _distance_to_start_edge, self.coordinate.column - _distance_to_start_edge)

    def _end_index(self) -> Tuple[int, int]:
        _distance_to_end_edge = min(self.board.row() - self.coordinate.row, self.board.column() - self.coordinate.column)
        return (self.coordinate.row + _distance_to_end_edge, self.coordinate.column + _distance_to_end_edge)

    def _coordinate_index(self):
        return min(self.coordinate.row, self.coordinate.column) - 1

    def _generate_line(self) -> List[GameMark]:
        _distance_to_edge = min(self.coordinate.row, self.coordinate.column) - 1
        _line = []
        _row = self.coordinate.row - _distance_to_edge
        _column = self.coordinate.column - _distance_to_edge   
        while _row in self.board.row_range() and _column in self.board.column_range():
            _line.append(self.board.get_mark(_row, _column))
            _row += 1
            _column += 1
        return _line

    def get_board_coordinate(self, list_index: int) -> Coordinate(int, int):
        return Coordinate(self.start[0] + list_index, self.start[1] + list_index)


# list of marks from the coordinate - up right to down left direction
class SecondaryDiagonalLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        # start and end index are coordinates
        self.start = self._start_index()
        self.end = self._end_index()
        # line is list of game mark
        self._line = self._generate_line()
        self._index = self._coordinate_index()
        
    @property
    def line(self) -> List[GameMark]:
        return self._line
    
    def _start_index(self) -> Tuple[int, int]:
        _distance_to_start_edge = min(self.coordinate.row - 1, self.board.column() - self.coordinate.column)
        return (self.coordinate.row - _distance_to_start_edge, self.coordinate.column + _distance_to_start_edge)

    def _end_index(self) -> Tuple[int, int]:
        _distance_to_end_edge = min(self.board.row() - self.coordinate.row, self.coordinate.column - 1)
        return (self.coordinate.row + _distance_to_end_edge, self.coordinate.column - _distance_to_end_edge)

    def _coordinate_index(self):
        return min(self.coordinate.row, self.board.column() + 1 - self.coordinate.column) - 1

    def _generate_line(self) -> List[GameMark]:
        # - 1 due to the board starts from 1
        _line = []
        # - 1 due to the board starts from 1
        _distance_to_edge = min(self.coordinate.row - 1, self.board.column() - self.coordinate.column) 

        _row = self.coordinate.row - _distance_to_edge
        _column = self.coordinate.column + _distance_to_edge        
        while _row in self.board.row_range() and _column in self.board.column_range():
            _line.append(self.board.get_mark(_row, _column))
            _row += 1
            _column -= 1
        return _line

    def get_board_coordinate(self, list_index: int) -> Coordinate(int, int):
        return Coordinate(self.start[0] + list_index, self.start[1] - list_index)


