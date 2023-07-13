from collections import defaultdict

class GameRule:
    WIN_LENGTH = 5
    NEXT_ROWS = [(1, 0),(-1, 0)]
    NEXT_COLUMNS = [(0, 1),(0, -1)]
    NEXT_LEFT_CROSS = [(-1, -1),(1, 1)]
    NEXT_RIGHT_CROSS = [(1, -1),(-1, 1)]

    @staticmethod
    def get_win_length():
        return GameRule.WIN_LENGTH

    @staticmethod
    def get_next_moves():
        return [GameRule.NEXT_ROWS, GameRule.NEXT_COLUMNS, GameRule.NEXT_LEFT_CROSS, GameRule.NEXT_RIGHT_CROSS]
    
    @staticmethod
    def is_over(board, row, column, player) -> bool:
            if GameRule().has_winner(board) or GameRule.is_draw(board):
                return True
            return False

    def is_prohibited_move(self, board, row, column, player) -> bool:
        lengths = self._get_lengths_from_position(board, row, column, player.get_mark())
        #if player = First_Player:
        # 3 x 3 prohibited
        if lengths.get(3, default=0) >= 2:
            return True
        elif lengths.get(4, default=0) >= 2:
            return True
        elif lengths.get(4, default=0) >= 2:
            pass

    def is_draw(board) -> bool:
        for i in board.row_range():
            for j in board.column_range():
                if board.is_empty(i, j):
                    return False
        return True

    def has_winner(self, board) -> bool:
        surroundings = self.get_next_moves()
        for i in board.row_range():
            for j in board.column_range():
                if not board.is_empty(i, j):
                    if self._get_length_of_one_line(board, i, j, board.get_mark(i, j), surroundings):
                        #has winner
                        return True
        return False

    def _get_length_of_one_line(self, board, i, j, mark, surroundings) -> bool:
        for directions in surroundings:
            _total_length = 1
            for next_direction in directions:
                _total_length += self._get_length_to_one_direction(board, i, j, mark, next_direction)
                if _total_length >= self.get_win_length():
                    return True
        return False

    def _get_length_to_one_direction(self, board, row, column, mark, next_direction, acceptable_empty = 0, mark_length = 0) -> int:
        next_row = row + next_direction[0]
        next_column = column + next_direction[1]
        if next_row in board.row_range() and next_column in board.column_range():
            if board.is_empty(next_row, next_column):
                acceptable_empty -= 1
                if acceptable_empty < 0:
                    return mark_length
                else:
                    mark_length = self._get_length_to_one_direction(board, next_row, next_column, mark, next_direction, acceptable_empty, mark_length)
            elif board.get_mark(next_row, next_column) == mark:
                mark_length += 1
                mark_length = self._get_length_to_one_direction(board, next_row, next_column, mark, next_direction, acceptable_empty, mark_length)
        return mark_length

    def _get_lengths_from_position(self, board, row, column, mark) -> dict:
        surroundings = self.get_next_moves()
        lengths = defaultdict(int) # 縦、横、左斜め、右斜めの長さ
        for directions in surroundings:
            one_length = self._get_combined_length(board, row, column, mark, directions[0], directions[1])
            another_length = self._get_combined_length(board, row, column, mark, directions[1], directions[0])
            
            if one_length == another_length:
                lengths[one_length] += 1
            else:
                lengths[one_length] += 1
                lengths[another_length] += 1
        return lengths

    def _get_combined_length(self, board, row, column, mark, direction1, direction2) -> int:
        length_with_no_empty = self._get_length_to_one_direction(board, row, column, mark, direction1, acceptable_empty=0)
        length_with_one_empty = self._get_length_to_one_direction(board, row, column, mark, direction2, acceptable_empty=1)
        return length_with_no_empty + length_with_one_empty + 1

