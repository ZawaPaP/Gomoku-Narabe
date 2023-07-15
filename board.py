from game_mark import GameMark
from typing import Tuple

class BoardCell:
    def __init__(self) -> None:
        self.mark = GameMark.EMPTY.value

class GameBoard:
    ROW = 9
    COLUMN = 9

    def __init__(self) -> None:
        self.board = [[BoardCell() for _ in range(self.column())] for _ in range(self.row())]

    def get_mark(self, row, column) -> GameMark:
        try:
            return self.board[row - 1][column - 1].mark
        except IndexError:
            raise IndexError

    def set_mark(self, row, column, mark) -> None:
        try:
            self.board[row - 1][column - 1].mark = mark
        except IndexError:
            raise IndexError

    def is_empty(self, row, column) -> bool:
        return self.get_mark(row, column) == GameMark.EMPTY.value

    def get_reach_position(self, mark) -> Tuple[int, int]:
        # row
        for row in self.row_range():
            marks = self.get_row_marks(row)
            if marks.count(mark) == (self.row() - 1) and marks.count(GameMark.EMPTY.value) == 1:
                column = marks.index(GameMark.EMPTY.value) + 1
                return row, column
        # col
        for column in self.column_range():
            marks = self.get_column_marks(column)
            if marks.count(mark) == (self.column() - 1) and marks.count(GameMark.EMPTY.value) == 1:
                row = marks.index(GameMark.EMPTY.value) + 1
                return row, column
            
        marks = self.get_left_to_right_cross_marks()
        if marks.count(mark) == (self.column() - 1) and marks.count(GameMark.EMPTY.value) == 1:
                i = marks.index(GameMark.EMPTY.value) + 1
                return i, i
            
        marks = self.get_right_to_left_cross_marks()
        if marks.count(mark) == (self.column() - 1) and marks.count(GameMark.EMPTY.value) == 1:
                i = marks.index(GameMark.EMPTY.value) + 1
                return i, self.row() + 1 - i
        return None

    def get_empty_corner(self) -> Tuple[int, int]:
        if self.is_empty(1, 1):
            return 1, 1
        elif self.is_empty(1, self.column()):
            return 1, self.column()
        elif self.is_empty(self.row(), 1):
            return self.row(), 1
        elif self.is_empty(self.row(), self.column()):
            return self.row(), self.column()
        else:
            return None

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

    def get_center_position(self) -> Tuple[int, int]:
        return (self.row() + 1) // 2, (self.column() + 1) // 2

    def get_row_marks(self, row: int) -> list:
        return [mark for mark in [self.get_mark(row, column) for column in self.column_range()]]

    def get_column_marks(self, column: int) -> list:
        return [mark for mark in [self.get_mark(row, column) for row in self.row_range()]]

    def get_left_to_right_cross_marks(self, row: int, column: int) -> list:
        marks = []
        # - 1 due to the board starts from 1
        _distance_to_top_left_cell = min(row - 1, column - 1)

        row -= _distance_to_top_left_cell
        column -= _distance_to_top_left_cell    
        while row in self.row_range() and column in self.column_range():
            marks.append(self.get_mark(row, column))
            row += 1
            column += 1
        return marks
    
    def get_right_to_left_cross_marks(self, row: int, column: int) -> list:
        marks = []
        # - 1 due to the board starts from 1
        _distance_to_top_right_edge = min(row - 1, self.column() - column) 

        row -= _distance_to_top_right_edge
        column += _distance_to_top_right_edge        
        while row in self.row_range() and column in self.column_range():
            marks.append(self.get_mark(row, column))
            row += 1
            column -= 1
        return marks

    def has_empty(window) -> bool:
        for i in window:
            if i == GameMark.EMPTY.value:
                return True
        return False
    