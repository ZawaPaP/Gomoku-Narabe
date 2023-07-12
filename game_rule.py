class GameRule:
    WIN_LENGTH = 4
    

    
    @staticmethod
    def is_over(board) -> bool:
            if GameRule().has_winner(board) or GameRule.is_draw(board):
                return True
            return False

    @staticmethod
    def __has_winner(board) -> bool:
        # row
        for i in board.row_range():
            if all(mark == board.get_mark(i, 1) and not board.is_empty(i, 1) for mark in board.get_row_marks(i)):
                return True
        # col
        for j in board.column_range():
            if all(mark == board.get_mark(1, j) and not board.is_empty(1, j) for mark in [board.get_mark(i, j) for i in board.row_range()]):
                return True
        # cross
        if all(mark == board.get_mark(1, 1) and not board.is_empty(1, 1) for mark in [board.get_mark(i, i)  for i in board.row_range()]):
            return True
            
        if all(mark == board.get_mark(1, 3) and not board.is_empty(1, 3) for mark in [board.get_mark(i, board.row() + 1 - i) for i in board.row_range()]):
            return True
        return False

    def is_draw(board) -> bool:
        for i in board.row_range():
            for j in board.column_range():
                if board.is_empty(i, j):
                    return False
        return True


    def has_winner(self, board) -> bool:
        next_rows = [(1, 0),(-1, 0)]
        next_columns = [(0, 1),(0, -1)]
        next_left_cross = [(-1, -1),(1, 1)]
        next_right_cross = [(1, -1),(-1, 1)]
        surroundings = [next_rows, next_columns, next_left_cross, next_right_cross]

        for i in board.row_range():
            for j in board.column_range():
                if not board.is_empty(i, j):
                    if self.check_winner(board, i, j, board.get_mark(i, j), surroundings):    
                        #has winner
                        return True
        return False

    def check_winner(self, board, i, j, mark, surroundings) -> bool:
        for surround in surroundings:
            mark_length_total = 1
            mark_length = 0
            for next_position in surround:
                mark_length_total += self.get_mark_length(board, i, j, mark, next_position, mark_length)
                if mark_length_total >= self.get_win_length():
                    return True
        return False

    def get_mark_length(self, board, i, j, mark, next_position, mark_length) -> int:
        if mark_length >= self.get_win_length() - 1: # win condition - 1
            return mark_length 

        next_row = i + next_position[0]
        next_column = j + next_position[1]
        if next_row in board.row_range() and next_column in board.column_range():
            if board.get_mark(next_row, next_column) == mark:
                mark_length += 1
                mark_length = self.get_mark_length(board, next_row, next_column, mark, next_position, mark_length)
            #次の周囲について同様にチェック
        return mark_length

    @staticmethod
    def get_win_length():
        return GameRule.WIN_LENGTH