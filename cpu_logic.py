import random
from typing import Tuple, List

class CPUStrategy:

    def generate_cpu_move(board, mark: str, opponent_marks: List[str]) -> Tuple[int, int]:
        return CPUStrategy.generate_low_level_cpu_move(board)
    
    @staticmethod
    def generate_low_level_cpu_move(board) -> Tuple[int, int]:
        while True:
            row = random.choice(board.row_range())
            column = random.choice(board.column_range())
            if board.is_empty(row, column):
                return row, column

    def generate_high_level_cpu_move(board, mark: str, opponent_marks: List[str]) -> Tuple[int, int]:
        #自分がリーチの場合、勝つ
        if board.get_reach_position(mark) is not None:
            return board.get_reach_position(mark)
        #相手がリーチか確認し、防ぐ
        for opponent_mark in opponent_marks:
            if board.get_reach_position(opponent_mark) is not None:
                return board.get_reach_position(opponent_mark)
        #中心が空いていたら取得 
        center_row, center_column = board.get_center_position()
        if board.is_empty(center_row, center_column):
            return center_row, center_column
        #空いていない場合、角が空いていれば角をランダム取得
        if board.get_empty_corner() is not None:
            return board.get_empty_corner()
        #空いている場所をランダム取得
        else:
            return CPUStrategy.generate_low_level_cpu_move(board)
