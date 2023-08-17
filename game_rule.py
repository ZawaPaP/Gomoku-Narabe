from board import GameBoard, Coordinate
from game_mark import GameMark
from game_analyzer import GameAnalyzer

class GameRule:
    WIN_LENGTH = 5

    @staticmethod
    def _win_length():
        return GameRule.WIN_LENGTH

    def is_over(self, board: GameBoard, coordinate: Coordinate, mark: GameMark, is_first_player: bool) -> bool:
        if self.is_prohibited_move(board, coordinate, mark, is_first_player):
            return True
        if self.is_win_move(board, coordinate, mark):
            return True
        if self.is_draw(board):
            return True
        return False

    def is_prohibited_move(self, board: GameBoard, coordinate: Coordinate, mark: GameMark, is_first_player: bool) -> bool:
        # overline
        if self.prohibited_long_chain(board, coordinate, mark, is_first_player):
            return True
        # if there is winner return and don't check 3x3 and 4x4 
        if self.is_win_move(board, coordinate, mark):
            return False
        # 4 x 4 prohibited
        # check if the move made more than 2 chain4 line
        if self.prohibited_chain_by_chain(board, coordinate, mark, is_first_player, GameAnalyzer.has_four_by_four):
            return True
        # 3 x 3 prohibited
        # check if the move made more than 2 chain3 line
        if self.prohibited_chain_by_chain(board, coordinate, mark, is_first_player, GameAnalyzer.has_three_by_three):
            return True
        return False

    def prohibited_long_chain(self, board: GameBoard, coordinate: Coordinate, mark: GameMark, is_first_player: bool) -> bool:
        if not is_first_player:
            return False
        _lines = board.get_lines_from_coordinate(coordinate)
        for line in _lines:
            if GameAnalyzer.get_length_of_chain(line, mark) > self._win_length():
                return True
        return False

    def prohibited_chain_by_chain(self, board: GameBoard, coordinate: Coordinate, mark: GameMark, is_first_player: bool , checker_method) -> bool:
        if not is_first_player:
            return False
        _lines = board.get_lines_from_coordinate(coordinate)
        if checker_method(_lines, mark):
            return True
        return False

    def is_win_move(self, board: GameBoard, coordinate: Coordinate, mark: GameMark) -> bool:
        _lines = board.get_lines_from_coordinate(coordinate)

        for line in _lines:
            if GameAnalyzer.get_length_of_chain(line, mark) >= self._win_length():
                return True
        return False

    @staticmethod
    def is_draw(board) -> bool:
        return board.is_full()
