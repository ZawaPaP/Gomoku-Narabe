class GameRule:
    @staticmethod
    def is_over(board) -> bool:
            if GameRule.has_winner(board) or GameRule.is_draw(board):
                return True
            return False

    @staticmethod
    def has_winner(board) -> bool:
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
