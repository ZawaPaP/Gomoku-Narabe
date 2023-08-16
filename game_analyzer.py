from board import GameBoard, Line, Coordinate
from game_mark import GameMark
from typing import Tuple, List, Set
from collections import Counter
from enum import Enum
import time

class ChainType(Enum):
    BOTH_SIDES_OPEN = "BothSidesOpen"
    ONE_SIDE_OPEN = "OneSideOpen"
    BOTH_SIDES_CLOSED = "BothSidesClosed"

class GameAnalyzer:
    @staticmethod
    def has_three_by_three(lines: List[Line], mark: GameMark) -> bool:
        chain3_count = 0
        for line in lines:
            if GameAnalyzer.has_chain3(line, mark):
                chain3_count += 1
                
        if chain3_count > 1:
            return True
        return False

    @staticmethod
    def has_four_by_four(lines: List[Line], mark: GameMark) -> bool:
        chain4_count = 0
        for line in lines:
            if GameAnalyzer.has_chain4(line, mark):
                chain4_count += 1
            
        if chain4_count > 1:
            return True
        return False

    @staticmethod
    def has_potential_for_chain5(line: Line, mark: GameMark) -> bool:
        if len(line._line) < 5:
            return False
        
        index = line._index
        _potential_length = 0
        
        for i in range(index, len(line.line)):
            if line._line[i] == GameMark.EMPTY.value or line._line[i] == mark:
                _potential_length += 1
                if _potential_length >= 5:
                    return True
            else:
                break
        for i in range(index, -1, -1):
            if line._line[i] == GameMark.EMPTY.value or line._line[i] == mark:
                _potential_length += 1
                if _potential_length >= 5:
                    return True
            else:
                break
        return False
    
    # check if the move made chain4 (1 empty acceptable)
    @staticmethod
    def has_chain4(line: Line, mark: GameMark) -> bool:
        if GameAnalyzer.has_chain4_with_jump(line, mark) or GameAnalyzer.has_chain4_without_jump(line, mark):
            return True
        return False  
    
    # check if the move made chain4 (1 empty acceptable)
    @staticmethod
    def has_chain3(line: Line, mark: GameMark) -> bool:
        if GameAnalyzer.has_chain4(line, mark):
            return False
        
        if GameAnalyzer.has_chain3_with_jump(line, mark) or GameAnalyzer.has_chain3_without_jump(line, mark):
            return True
        return False      

    @staticmethod
    # check if the move made chain3 (1 empty acceptable)
    def has_chain2(line: Line, mark: GameMark) -> bool:
        # if chain is longer than 2, False
        if GameAnalyzer.has_chain3(line, mark):
            return False
        if not GameAnalyzer.get_length_of_chain(line, mark) == 2:
            return False

        length = 2
        for i in range(len(line.line) - length + 1):
            if all(item == mark for item in line.line[i:i+length]):
                start_index = i
                end_index = i + length - 1
                if GameAnalyzer.get_window_sides_type(line, start_index, end_index) == ChainType.BOTH_SIDES_OPEN:
                    return True
        return False
    
    @staticmethod
    def has_any_chain(line: Line, mark: GameMark) -> bool:
        if GameAnalyzer.get_length_of_chain(line, mark) < 2:
            return False
        
        length = 2
        for i in range(len(line.line) - length + 1):
            if all(item == mark for item in line.line[i:i+length]):
                start_index = i
                end_index = i + length - 1
                if GameAnalyzer.get_window_sides_type(line, start_index, end_index) == ChainType.BOTH_SIDES_OPEN:
                    return True
        return False
    

    @staticmethod
    def has_chain4_without_jump(line: Line, mark: GameMark) -> bool:
        if not GameAnalyzer.get_length_of_chain(line, mark) == 4:
            return False
        
        length = 4
        
        for i in range(len(line.line) - length + 1):
            if all(item == mark for item in line.line[i:i+length]):
                start_index = i
                end_index = i + length - 1
                
                if GameAnalyzer.get_window_sides_type(line, start_index, end_index) == ChainType.BOTH_SIDES_CLOSED:
                    return False
                return True
        return False

    @staticmethod
    def has_chain4_with_jump(line: Line, mark: GameMark) -> bool:
        # if chain is longer than 4, it is not chain4
        if GameAnalyzer.get_length_of_chain(line, mark) >= 4:
            return False
        
        # get windows contain finding_length marks
        _windows = GameAnalyzer._get_windows(line, mark, finding_length=4)
        for start, end in _windows:
            # if chain is longer than 4, it is not chain4
            if not GameAnalyzer.is_chain_one_jump(line.line[start: end + 1]):
                continue
            
            if not GameAnalyzer.get_window_sides_type(line, start, end) == ChainType.BOTH_SIDES_CLOSED:
                return True
        return False  

    @staticmethod
    def has_chain3_without_jump(line: Line, mark: GameMark) -> bool:
        if not GameAnalyzer.get_length_of_chain(line, mark) == 3:
            return False
        
        length = 3
        
        for i in range(len(line.line) - length + 1):
            if all(item == mark for item in line.line[i:i+length]):
                start_index = i
                end_index = i + length - 1
                
                if GameAnalyzer.get_window_sides_type(line, start_index, end_index) == ChainType.BOTH_SIDES_OPEN:
                    return True
        return False

    @staticmethod
    def has_chain3_with_jump(line: Line, mark: GameMark) -> bool:
        # if chain is longer than 4, it is not chain4
        if GameAnalyzer.get_length_of_chain(line, mark) >= 3:
            return False
        
        # get windows contain finding_length marks
        _windows = GameAnalyzer._get_windows(line, mark, finding_length=3)
        for start, end in _windows:
            # if chain is longer than 4, it is not chain4
            if not GameAnalyzer.is_chain_one_jump(line.line[start: end + 1]):
                continue
            
            if GameAnalyzer.get_window_sides_type(line, start, end) == ChainType.BOTH_SIDES_OPEN:
                return True
        return False  

    @staticmethod
    def get_length_of_chain(line: Line, mark: GameMark) -> int:
        _length = 0
        index = line._index
        for i in range(index, len(line.line)):
            if line._line[i] == mark:
                _length += 1
            else:
                break
        for i in range(index - 1, -1, -1):
            if line._line[i] == mark:
                _length += 1
            else:
                break
            
        return _length

    # return the window's start and end index 
    # if the window has finding_length's marks in the finding_length + 1 window size
    # because chain accepts 1 jump
    @staticmethod
    def _get_windows(line: Line, mark: GameMark, finding_length: int) -> List[Tuple[int, int]]:
        # window size = 1 + finding length because accept 1 jump
        # window is tuple of start and end index
        # get all windows of the line
        _all_windows = [(i, i + finding_length) for i in range(len(line.line) - finding_length)]
        # get window only if having finding_length marks
        windows_with_marks = [(start, end) for start, end in _all_windows if line.line[start: end + 1].count(mark) == finding_length]
        return windows_with_marks

    @staticmethod
    def get_window_sides_type(line: Line, start: int, end: int) -> ChainType:
        open_count = 0
        if end + 1 < len(line.line) and line.line[end + 1] == GameMark.EMPTY.value:
            open_count += 1
        if  start - 1 >= 0 and line.line[start - 1] == GameMark.EMPTY.value:
            open_count += 1
        
        if open_count == 2:
            return ChainType.BOTH_SIDES_OPEN
        if open_count == 1:
            return ChainType.ONE_SIDE_OPEN
        return ChainType.BOTH_SIDES_CLOSED

    @staticmethod
    def get_chain_gaps(line: Line):
        gaps = []
        # use window (size=3) and if contains 2 unique mark and 1 empty, return empty coordinate
        size = 2
        for i in range(len(line.line) - size):
            window = line.line[i : i+ size + 1]
            mark_set = set(window)
            if window.count(GameMark.EMPTY.value) == 1 and len(mark_set) == 2:
                gaps.append(i + window.index(GameMark.EMPTY.value))
        return gaps

    # Check if the data contains only one mark
    @staticmethod
    def is_chain_no_jump(data: List[GameMark]) -> bool:
        # Find the unique non-empty mark
        non_empty_marks = set([mark for mark in data if mark != GameMark.EMPTY])
        
        # If there's more than one mark, return False
        if len(non_empty_marks) != 1:
            return False
        # Check if the count of the non-empty mark is length - 1
        mark_count = data.count(list(non_empty_marks)[0])
        if mark_count == len(data):
            return True
        return False

    # check if the data has only 1 jump between the unique marks
    @staticmethod
    def is_chain_one_jump(data: List[GameMark]) -> bool:
        if data[0] == GameMark.EMPTY.value or data[-1] == GameMark.EMPTY.value:
            return False
        
        # Find the unique non-empty mark
        non_empty_marks = set([mark for mark in data if mark != GameMark.EMPTY.value])
        # If there's more than one mark, return False
        if len(non_empty_marks) != 1:
            return False

        # Check if the count of the non-empty mark is length - 1
        mark_count = data.count(list(non_empty_marks)[0])
        if mark_count != len(data) - 1:
            return False
        return data.count(GameMark.EMPTY.value) == 1

    @staticmethod
    def _find_empty_index(line: Line, start: int, end: int) -> int:
        for i in range(start, end + 1):
            if line.line[i] == GameMark.EMPTY.value:
                return i
        return None # This should never be reached

    # return list of coordinates
    # get surrounding cells' coordinates of marked cells
    # default distance from marked cells is 2 due to 1 jump acceptable
    @staticmethod
    def get_marked_surroundings(board: GameBoard, distance=2) -> Set[Coordinate]:
        marked_cells = GameAnalyzer._get_marked_cells(board)
        surrounding_coordinates = set()
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in directions:
            # d = -distance ~ distance 
            for d in range(-distance, distance + 1):
                for cell in marked_cells:
                    x, y = cell.row + d * dx, cell.column + d * dy
                    # d == 0 means marked cell, skip to add
                    if x in board.row_range() and y in board.column_range():
                        if board.is_cell_empty(x, y):
                            surrounding_coordinates.add(Coordinate(x, y))
        # remove the marked cell's coordinate from the set if exists
        return surrounding_coordinates

    @staticmethod
    def _get_marked_cells(board: GameBoard) -> List[Coordinate]:
        _marked_cells_set = set()
        for i in board.row_range():
            for j in board.column_range():
                if board.get_mark(i, j) != GameMark.EMPTY.value:
                    _marked_cells_set.add(Coordinate(i, j))
        return list(_marked_cells_set)
