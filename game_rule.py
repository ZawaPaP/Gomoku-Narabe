from collections import defaultdict
from game_mark import GameMark

from typing import Optional, List, Tuple

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
    def get_surroundings():
        return [GameRule.NEXT_ROWS, GameRule.NEXT_COLUMNS, GameRule.NEXT_LEFT_CROSS, GameRule.NEXT_RIGHT_CROSS]
    
    def is_over(self, board, row, column, player) -> bool:
            if self.has_winner(board, row, column) or self.is_draw(board) or self.is_prohibited_move(board, row, column, player):
                return True
            return False

    def is_prohibited_move(self, board, row, column, player) -> bool:
        _mark = board.get_mark(row, column)
        _row_marks = board.get_row_marks(row)
        _column_marks = board.get_column_marks(column)
        _left_right_cross_marks = board.get_left_to_right_cross_marks(row, column)
        _right_to_left_cross_marks = board.get_right_to_left_cross_marks(row, column)
        # early return
        # 1 ya Stringというのは必ずメモリロケーションがあるため、イコールを使う。Noneの場合のみ is / is notをつかう                
        if player.get_play_order() != 1:
            return False
        
        # overline
        if self._is_prohibited_over_line(board, row, column, player):
            print("prohibited move: over line length")
            return True

        # 3 x 3 prohibited
        three_line_count = 0
        if self._has_three_line(_mark, _row_marks, row):
            three_line_count += 1
        if self._has_three_line(_mark, _column_marks, column):
            three_line_count += 1
        if self._has_three_line(_mark, _left_right_cross_marks, min(row, column)):
            three_line_count += 1
        if self._has_three_line(_mark, _right_to_left_cross_marks, min(row, board.column() - column + 1)):
            three_line_count += 1
        if three_line_count >= 2:
            print(f"prohibited move: three by three ({row, column})")
            return True
        
        four_line_count = 0
        if self._has_four_line(_mark, _row_marks, row):
            four_line_count += 1
        if self._has_four_line(_mark, _column_marks, column):
            four_line_count += 1
        if self._has_four_line(_mark, _left_right_cross_marks, min(row, column)):
            four_line_count += 1
        if self._has_four_line(_mark, _right_to_left_cross_marks, min(row, board.column() - column + 1)):
            four_line_count += 1
        if four_line_count >= 2:
            print(f"prohibited move: four by four ({row, column})")
            return True
        return False

    def _is_prohibited_over_line(self, board, row, column, player) -> bool:
        if player.get_play_order() != 1:
            return False
        longest_length = self._get_longest_length(board, row, column)
        if longest_length > self.get_win_length():
            return True
        return False

    def is_draw(self, board) -> bool:
        for i in board.row_range():
            for j in board.column_range():
                if board.is_empty(i, j):
                    return False
        return True

    def has_winner(self, board, row, column) -> bool:
        length = self._get_longest_length(board, row, column)
        if length >= self.get_win_length():
            print(row, column)
            return True
        return False

    def _get_longest_length(self, board, row, column) -> int:
        _mark = board.get_mark(row, column)
        _row_marks = board.get_row_marks(row)
        _column_marks = board.get_column_marks(column)
        _left_right_cross_marks = board.get_left_to_right_cross_marks(row, column)
        _right_to_left_cross_marks = board.get_right_to_left_cross_marks(row, column)

        longest_length = 1
        _row_length = self._get_no_empty_length(column, _mark, _row_marks)
        _column_length = self._get_no_empty_length(row, _mark, _column_marks)
        _left_right_cross_length = self._get_no_empty_length(min(row, column), _mark, _left_right_cross_marks)
        _right_left_cross_length = self._get_no_empty_length(min(row, board.column() + 1 -column), _mark, _right_to_left_cross_marks)
    
        print(_row_length, _column_length, _left_right_cross_length, _right_left_cross_length)
        
        longest_length = max(_row_length, _column_length, _left_right_cross_length, _right_left_cross_length)
        return longest_length
    
    def _get_no_empty_length(self, index, mark, marks) -> int:
        # left, right is relevant distance from the index 
        left_index = index * (-1) + 1
        right_index = len(marks) - index
        # change left and right to sequence's edge from the mark.
        for i in range(1, len(marks) + 1):
            # i is range 1 to board.row() + 1
            if marks[i - 1] != mark:
                if i - index < 0:
                    left_index = max(left_index, i - index + 1)
                if i - index > 0:
                    right_index = min(right_index, i - index - 1)
        # + 1 as own mark
        return right_index - left_index + 1


    # return list with finding_length with the index from the marks list (1 empty acceptable)
    def _has_three_line(self, mark, marks, index) -> bool:
        # List[Tuple[int, int]] > start and end index of window includes finding_length
        windows_index = self._get_windows_with_mark(mark, marks, index, finding_length = 3)
        for window in windows_index:
            if self._is_both_side_empty(window[0], window[1], marks, mark):
                return True
        return False            

    def _has_four_line(self, mark, marks, index) -> bool:
        # List[Tuple[int, int]] > start and end index of window includes finding_length
        windows_index = self._get_windows_with_mark(mark, marks, index, finding_length = 4)
        for window in windows_index:
            if self._is_single_side_empty(window[0], window[1], marks, mark):
                return True
        return False  

    # return list with finding_length with the index from the marks list (1 empty acceptable)
    def _get_windows_with_mark(self, mark, marks, index, finding_length) -> List[Tuple[int, int]]:
        windows = self._get_window_list(marks, index, finding_length)
        windows_with_marks = []
        # if window include finding_length marks, append the start and end index, return
        for window in windows:
            if self._count_elements_in_range(marks, window[0], window[1], mark) == finding_length:
                windows_with_marks.append(window)
        return windows_with_marks


    # return list with finding_length with the index from the marks list (1 empty acceptable)
    def _get_window_list(self, marks, index, finding_length) -> List[Tuple[int, int]]:
        
        #index is range 1 to 9
        _left_pointer = index - finding_length
        _right_pointer = _left_pointer + finding_length
        windows = []

        # get and append the start and end index of (finding_length + 1) size window in the marks range
        while _left_pointer <= index:
            if _left_pointer <= 0 or _right_pointer > len(marks):
                _left_pointer += 1
                _right_pointer += 1
                continue
            windows.append((_left_pointer, _right_pointer))
            _left_pointer += 1
            _right_pointer += 1
        return windows


    # window includes (length - 1) mark
    # left and right are index of window in the board (1 - 9)
    def _is_both_side_empty(self, left, right, marks, mark) -> bool:
        window = marks[left - 1 : right] 
        # if there is no empty (there is other mark)
        if not GameMark.EMPTY.value in window:
            return False
        
        outcast_index = self._find_index_except(window, mark)
        # if outcast is in the first cell, check if other side is empty
        if outcast_index == 0:
            if right < len(marks) and marks[right] == GameMark.EMPTY.value:
                return True
        # if outcast is in the last cell, check if other side is empty
        elif outcast_index == len(window) - 1:
            if  left - 2 >= 0 and marks[left - 2] == GameMark.EMPTY.value:
                return True
        # if outcast is not side, check both side        
        else:
            if right < len(marks) and left - 2 >= 0 and marks[left - 2] == GameMark.EMPTY.value and marks[right] == GameMark.EMPTY.value:
                return True
        return False
                
    def _is_single_side_empty(self, left, right, marks, mark) -> bool:
        window = marks[left - 1: right]
        outcast_index = self._find_index_except(window, mark)
        
        if window[outcast_index] == GameMark.EMPTY.value:
            return True

        if outcast_index == 0:
            if right < len(marks) and marks[right] == GameMark.EMPTY.value :
                return True
        
        if outcast_index == len(window) - 1:            
            if left - 2 >= 0 and marks[left - 2] == GameMark.EMPTY.value:
                return True
        return False

        
    def _find_index_except(self, data: list, target) -> int:
        for i in range(len(data)):
            if data[i] != target:
                return i
        return -1

    def _count_elements_in_range(self, data, start, end, target) -> int:
        count = 0
        try:
            for i in range(start, end + 1):
                # start and end starts from 1, but list index starts from 0
                if data[i - 1] == target:
                    count += 1
            return count
        except IndexError:
            return count
