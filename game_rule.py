from board import GameBoard, Coordinate, Line, RowLine, ColumnLine, CrossLeftToRightLine, CrossRightToLeftLine
from player import Player

class GameRule:
    WIN_LENGTH = 5

    @staticmethod
    def _win_length():
        return GameRule.WIN_LENGTH

    def is_over(self, board: GameBoard, coordinate: Coordinate, player: Player) -> bool:
        if self.is_prohibited_move(board, coordinate, player) or self.has_winner(board, coordinate) or self.is_draw(board):
            return True
        return False

    def is_prohibited_move(self, board: GameBoard, coordinate: Coordinate, player: Player) -> bool:
        # early return            
        if not player.is_first_player():
            return False
        
        # overline
        if self._is_over_line(board, coordinate, player):
            print(f"prohibited move: over line length {coordinate.row, coordinate.column}")
            return True

        # if there is winner return and don't check 3x3 and 4x4 
        if self.has_winner(board, coordinate):
            return False
        
        # 4 x 4 prohibited
        if self._has_four_by_four(board, coordinate):
            print(f"prohibited move: four by four {coordinate.row, coordinate.column}")
            return True
        
        # 3 x 3 prohibited
        if self._has_three_by_three(board, coordinate):
            print(f"prohibited move: three by three {coordinate.row, coordinate.column}")
            return True
        return False


    def _is_over_line(self, board: GameBoard, coordinate: Coordinate, player: Player) -> bool:
        # early return            
        if not player.is_first_player():
            return False
        
        longest_length = board.get_longest_length(coordinate)
        if longest_length > self._win_length():
            return True
        return False

    def _has_three_by_three(self, board: GameBoard, coordinate: Coordinate) -> bool:
        chain3_count = 0
        if RowLine(board, coordinate).has_chain3():
            chain3_count += 1
        if ColumnLine(board, coordinate).has_chain3():
            chain3_count += 1
        if CrossLeftToRightLine(board, coordinate).has_chain3():
            chain3_count += 1
        if CrossRightToLeftLine(board, coordinate).has_chain3():
            chain3_count += 1
        if chain3_count > 1:
            return True
        return False

    def _has_four_by_four(self, board: GameBoard, coordinate: Coordinate) -> bool:
        chain4_count = 0
        if RowLine(board, coordinate).has_chain4():
            chain4_count += 1
        if ColumnLine(board, coordinate).has_chain4():
            chain4_count += 1
        if CrossLeftToRightLine(board, coordinate).has_chain4():
            chain4_count += 1
        if CrossRightToLeftLine(board, coordinate).has_chain4():
            chain4_count += 1
        if chain4_count > 1:
            return True
        return False

    def has_winner(self, board: GameBoard, coordinate: Coordinate) -> bool:

        length = board.get_longest_length(coordinate)
        if length >= self._win_length():
            print(length)
            return True
        return False

    @staticmethod
    def is_draw(board) -> bool:
        for i in board.row_range():
            for j in board.column_range():
                if board.is_empty(i, j):
                    return False
        return True

