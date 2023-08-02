from game_mark import GameMark
from error import OutRangeCoordinateError, NoOutCastMarkError, NoLineExistError
from typing import Tuple, List, Dict

class BoardCell:
    def __init__(self) -> None:
        self.mark = GameMark.EMPTY.value

class Coordinate:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column


    def is_in_board(self) -> bool:
        if self.row in GameBoard.row_range() and self.column in GameBoard.column_range():
            return True
        
        else:
            raise OutRangeCoordinateError(f"{self.row, self.column}")


class GameBoard:
    ROW = 9
    COLUMN = 9

    def __init__(self) -> None:
        self.board = [[BoardCell() for _ in range(self.column())] for _ in range(self.row())]

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

    def set_mark(self, coordinate: Coordinate, mark: GameMark) -> None:
        self.board[coordinate.row - 1][coordinate.column - 1].mark = mark

    def remove_mark(self, coordinate: Coordinate) -> None:
        self.board[coordinate.row - 1][coordinate.column - 1].mark = GameMark.EMPTY.value

    def is_empty(self, row, column) -> bool:
        return self.get_mark(row, column) == GameMark.EMPTY.value

    def get_longest_length(self, coordinate: Coordinate) -> int:
        _mark = self.get_mark(coordinate.row, coordinate.column)
        # get mark-length 
        _longest_length = max(
            RowLine(self, coordinate).get_length_without_jump(_mark), 
            ColumnLine(self, coordinate).get_length_without_jump(_mark),
            CrossLeftToRightLine(self, coordinate).get_length_without_jump(_mark),
            CrossRightToLeftLine(self, coordinate).get_length_without_jump(_mark)
        )
        return _longest_length

class Line:
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        self.board = board
        self.coordinate = coordinate
        self._line = None
        self._index = None

    @property
    def line(self) -> List[GameMark]:
        raise NotImplementedError()

    @property
    # return index in the line 
    def index(self) -> int:
        raise NotImplementedError()

    def get_mark(self, index: int) -> GameMark:
        return self.line[index - 1]
    
    def is_marked_position(self, index:int) -> bool:
        if self.line[index - 1] == GameMark.EMPTY.value:
            return False
        return True
        
    def is_in_range(self, index: int) -> bool:
        if index in range(1, len(self.line) + 1):
            return True
        return False

    def is_line_empty(self) -> bool:
        if self.line == None:
            raise NoLineExistError()
        return all(mark == GameMark.EMPTY.value for mark in self.line)


    # check if the move made chain4 (1 empty acceptable)
    def has_chain4(self) -> bool:
        # if chain is longer than 4, it is not chain4
        _mark = self.get_mark(self.index)
        if self.get_length_without_jump(_mark) > 4:
            return False
        # window_size = finding mark-length + 1
        # because some cases accept 1 jump
        _windows = self._get_windows(finding_length=4)
        for window in _windows:
            left, right = window
            if self._is_single_side_empty(left, right):
                return True
        return False

    # check if the move made chain3 (1 empty acceptable)
    def has_chain3(self) -> bool:
        # if chain is longer than 3, False
        if self.has_chain4():
            return False
        # get windows which has 3 marks in window (size 4)
        # _windows is list of tuple (window left index, window right index)
        _windows = self._get_windows(finding_length=3)
        for window in _windows:
            left, right = window
            if self._is_both_side_empty(left, right):
                return True
        return False            

    def get_length_without_jump(self, mark) -> int:
        length = 0
        # check next left from the reference point (_index)
        for i in range(1, len(self.line)):
            if self.is_in_range(self.index - i) and self.get_mark(self.index - i) == mark:
                length += 1
            else:
                break
        # check next right from the reference point (_index)
        for i in range(1, len(self.line)):
            if self.is_in_range(self.index + i) and self.get_mark(self.index + i) == mark:
                length += 1
            else:
                break
        return length + 1

    # return window start and end index if the window has finding_length's marks

    def _get_windows(self, finding_length: int) -> List[Tuple[int, int]]:
        #index is range 1 to 9
        # index is the moved position
        _index = self.index
        # window size = 1 + finding length because accept 1 jump
        window_size = finding_length + 1
        # all windows from the index
        _windows = [(_index - i, _index - i + window_size - 1) for i in range(window_size)]
        # get window only if in board range
        _windows_in_range = [(start, end) for start, end in _windows if 1 <= start <= len(self.line) and 1 <= end <= len(self.line)]
        # get window only if having window-size - 1 marks 
        windows_with_mark = [(start, end) for start, end in _windows_in_range if self.line[start - 1: end].count(self.get_mark(_index)) == finding_length]
        
        return windows_with_mark

    # already know window contains (length - 1) marks
    # return True if window contains (length - 1) marks and both side empty
    # because finding_length = window_length - 1 (accept 1 jump)
    def _is_both_side_empty(self, left: int, right: int) -> bool:
        window = self.line[left - 1 : right] 
        # return False if there is no empty (there is other mark)
        if not GameMark.EMPTY.value in window:
            return False
        
        outcast_index = self._outcast_mark_index(window)
        # if outcast is in the first cell, check if other side is empty
        if outcast_index == 0:
            if right < len(self.line) and self.line[right] == GameMark.EMPTY.value:
                return True
        # if outcast is in the last cell, check if other side is empty
        elif outcast_index == len(window) - 1:
            if  left - 2 >= 0 and self.line[left - 2] == GameMark.EMPTY.value:
                return True
        # if outcast is not side, check both side        
        else:
            if right < len(self.line) and left - 2 >= 0 and self.line[left - 2] == GameMark.EMPTY.value and self.line[right] == GameMark.EMPTY.value:
                return True
        return False

    # already know window contains (length - 1) marks
    # return True if window contains (length - 1) marks and at least one side empty
    # because finding_length = window_length - 1 (accept 1 jump)
    def _is_single_side_empty(self, left: int, right: int) -> bool:
        window = self.line[left - 1: right]
        outcast_index = self._outcast_mark_index(window)
        
        if window[outcast_index] == GameMark.EMPTY.value:
            return True

        if outcast_index == 0:
            if right < len(self.line) and self.line[right] == GameMark.EMPTY.value:
                return True
        
        if outcast_index == len(window) - 1:            
            if left - 2 >= 0 and self.line[left - 2] == GameMark.EMPTY.value:
                return True
        return False
        
    def _outcast_mark_index(self, data) -> int:
        for i in range(len(data)):
            if data[i] != self.get_mark(self.index):
                return i
        raise NoOutCastMarkError()

# list of marks from the coordinate - row direction
class RowLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        self._index = coordinate.column
        self._line = [mark for mark in [board.get_mark(coordinate.row, column) for column in board.column_range()]]

    @property
    def line(self) -> List[GameMark]:
        return self._line

    @line.setter
    def line(self, value: List[GameMark]) -> None:
        self._line = value

    @property
    # return index in the line 
    def index(self) -> int:
        return self._index
    
    @index.setter
    def index(self, value: int) -> None:
        self._index = value

# list of marks from the coordinate - column direction
class ColumnLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        self._index = coordinate.row
        self._line = [mark for mark in [board.get_mark(row, coordinate.column) for row in board.row_range()]]
    
    @property
    def line(self) -> List[GameMark]:
        return self._line

    @property
    # return index in the line 
    def index(self) -> int:
        return self._index


# list of marks from the coordinate - up left to down right direction
class CrossLeftToRightLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        self._index = min(coordinate.row, coordinate.column)
        self._line = self._create_line()
        
    
    @property
    def line(self) -> List[GameMark]:
        return self._line
    
    @property
    def index(self) -> int:
        return self._index

    def _create_line(self) -> List[GameMark]:
        _distance_to_edge = min(self.coordinate.row - 1, self.coordinate.column - 1)
        _line = []
        _row = self.coordinate.row - _distance_to_edge
        _column = self.coordinate.column - _distance_to_edge   
        while _row in self.board.row_range() and _column in self.board.column_range():
            _line.append(self.board.get_mark(_row, _column))
            _row += 1
            _column += 1
        return _line


# list of marks from the coordinate - up right to down left direction
class CrossRightToLeftLine(Line):
    def __init__(self, board: GameBoard, coordinate: Coordinate) -> None:
        super().__init__(board, coordinate)
        self._index = min(coordinate.row, board.column() + 1 - coordinate.column)
        self._line = self._create_line()

    @property
    def line(self) -> List[GameMark]:
        return self._line
    
    @property
    # return index in the line 
    def index(self) -> int:
        return self._index

    def _create_line(self) -> List[GameMark]:
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
