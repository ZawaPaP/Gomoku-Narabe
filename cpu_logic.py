import random
from typing import Tuple, List
from board import GameBoard, Coordinate


class CPULogic:
    def __init__(self, cpu_player) -> None:
        self.cpu_player = cpu_player

    @staticmethod
    def generate_move(board) -> Coordinate:
        pass

class DumbCPULogic(CPULogic):
    def __init__(self, cpu_player) -> None:
        super().__init__(cpu_player)
    
    @staticmethod
    def generate_move(board) -> Coordinate:
        while True:
            row = random.choice(board.row_range())
            column = random.choice(board.column_range())
            coordinate = Coordinate(row, column)
            if board.is_empty(coordinate.row, coordinate.column):
                return coordinate


class HighCPULogic(CPULogic):
    
    def return_zero():
        return 0

    def return_sum_number(number):
        board = GameBoard()
        for i in board.row_range():
            for j in board.column_range():
                board.set_mark(i, j, number)
        
        result = 0
        for i in board.row_range():
            result += sum(board.get_row_marks(i))
        return result

    def find_make_win(self, data):
        board = GameBoard()
        result = []
        
        length = 0
        for i in range(1, len(data) + 1):
            if board.get_no_empty_length(i, "o", data) == GameRule._win_length():
                result.append(GameRule._win_length())
            else:
                result.append(data[i - 1])
        return result

    def get_scoring_list(self, marks):
        board = GameBoard()
        result = []
        
        length = 0
        for i in range(1, len(marks) + 1):
            if marks[i - 1] == "o":
                result.append(marks[i - 1])
            elif board.has_chain4(i, "o", marks):
                result.append(5)
            elif board.has_chain3(i, "o", marks):
                result.append(4)
            else:
                result.append(marks[i - 1])
        return result

