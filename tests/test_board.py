import pytest
from error import NoOutCastMarkError
from board import GameBoard, Coordinate, RowLine, ColumnLine, PrincipalDiagonalLine, SecondaryDiagonalLine
from game_analyzer import GameAnalyzer
from typing import List


class Board(GameBoard):
    # create coordinate class simply
    def c(self, row, column):
        return Coordinate(row, column)
    
    # only use to create test board 
    def set_line(self, row, marks):
        for index, mark in enumerate(marks):
            self.set_mark(self.c(row, index + 1), mark)

# example board for test
def _create_test_board():
    board = Board()
    board.set_line(1, ["x", "o", "o", "x", "x", "x", "x", "o", " "])
    board.set_line(2, ["x", "o", "x", "o", " ", "o", " ", "o", "o"])
    board.set_line(3, ["x", "x", "x", "x", " ", "x", " ", "o", "o"])
    board.set_line(4, [" ", "x", "o", "o", "o", "o", "x", "x", "x"])
    board.set_line(5, ["o", "o", "o", "o", "o", "o", "o", "o", "o"])
    board.set_line(6, ["x", "o", "o", "o", " ", "o", " ", "x", "x"])
    board.set_line(7, ["x", "x", "x", "x", "x", "x", "x", "x", "x"])
    board.set_line(8, ["o", "o", "o", "o", "x", "o", "x", "x", "x"])
    board.set_line(9, [" ", "o", "o", "o", " ", "x", "x", "x", "x"])
    return board

class TestBoard:

    class TestHasChain3:
        @pytest.fixture
        def board(self):
            return _create_test_board()

        @pytest.mark.parametrize('coordinate, mark, marks, expected_result', [
            # move is marked index (range: 1 to len(marks))
            (Coordinate(1, 2), "o", [" ", "o", "o", "o", " ", " "], True),     # basic chain3 without jump
            (Coordinate(1, 2), "o", [" ", "o", "o", " ", " ", " "], False),    # no chain 3
            (Coordinate(1, 2), "o", [" ", "o", "o", "x", "o", " "], False),    # no chain 3
            (Coordinate(1, 2), "o", ["o", "o", "o", " ", " ", " "], False),    # chain3 but only one-side empty, edge
            (Coordinate(1, 2), "o", ["x", "o", "o", "o", " ", " "], False),    # chain3 but only one-side empty, marked
            (Coordinate(1, 2), "o", ["o", "o", "o", "x", " ", " "], False),    # chain3 but not both-side empty, edge and marked
            (Coordinate(1, 2), "o", ["x", "o", "o", "o", "x", " "], False),    # chain3 but not both-side empty, marked
            (Coordinate(1, 2), "o", [" ", "o", "o", " ", "o", " "], True),     # chain3 with jump
            (Coordinate(1, 2), "o", [" ", "o", "o", " ", "o", "x"], False),    # chain3 with jump but only one-side empty, one side other mark
            (Coordinate(1, 2), "o", ["o", " ", "o", "o", " ", " "], False),    # chain3 with jump but only one-side empty, one side edge
            (Coordinate(1, 2), "o", ["o", "o", "o", "o", " ", " "], False),    # having chain4, one side empty
            (Coordinate(1, 2), "o", [" ", "o", "o", "o", "o", " "], False),    # having chain4, both side empty
            (Coordinate(1, 2), "o", ["x", "o", "o", "o", "o", "x"], False),    # having chain4, both side filled
            (Coordinate(1, 2), "o", [" ", "o", "o", "o", " ", "o"], False),    # having chain4 with jump
            (Coordinate(1, 2), "o", ["o", "o", "o", "o", "o", "o"], False),    # having chain4+
            (Coordinate(1, 3), "o", ["o", "o", "x", "o", "o", "o"], False),    # having chain4+
        ])

        def test_has_chain3(self, board, coordinate, mark, marks, expected_result):
            _line = RowLine(board, coordinate)
            _line._line = marks
            assert GameAnalyzer.has_chain3(_line, mark) == expected_result   


    class TestHasChain4:
        @pytest.fixture
        def board(self):
            return _create_test_board()
        
        @pytest.mark.parametrize('coordinate, mark, marks, expected_result', [
            # move is marked index (range: 1 to len(marks))
            (Coordinate(1, 2), "o", [" ", "o", "o", "o", "o", " "], True),     # chain4 
            (Coordinate(1, 2), "o", [" ", "o", "o", "o", " ", " "], False),    # not having chain 4
            (Coordinate(1, 2), "o", [" ", "o", "o", "x", "o", "o"], False),    # not having chain 4
            (Coordinate(1, 1), "o", ["o", "o", "x", "o", "o", "o"], False),    # not having chain 4
            (Coordinate(1, 2), "o", ["o", "o", "o", "o", " ", " "], True),    # chain4, one-side empty
            (Coordinate(1, 2), "o", [" ", "o", "o", "o", " ", "o"], True),    # chain4 with jump
            (Coordinate(1, 2), "o", ["o", "o", "o", "o", "x", " "], False),    # chain4 but neither side empty
            (Coordinate(1, 2), "o", ["o", "o", "o", "o"], False),    # chain4 but neither side empty, edge
            (Coordinate(1, 2), "o", ["o", "o", "o", "o", "o", " "], False),    # having chain5
            (Coordinate(1, 3), "o", ["o", " ", "o", "o", "o", "o"], True),    # having chain6 with jump but also has chain4 no jump
            (Coordinate(1, 2), "o", ["x", "o", "o", "o", "o", "o", "x"], False),    # having chain5, neither sides empty
            (Coordinate(1, 2), "o", ["o", "o", "o", "o", "o", "o"], False),    # having chain4+
        ])
    
        def test_has_chain4(self, board, coordinate, mark, marks, expected_result):
            _line = RowLine(board, coordinate)
            _line._line = marks

            assert GameAnalyzer.has_chain4(_line, mark) == expected_result    

    """
    class TestIsSingleSideEmpty:
        @pytest.fixture
        def board(self):
            return _create_test_board()
        
        # check window[left, right]'s side are empty
        @pytest.mark.parametrize("coordinate, left, right, expected_result", [
            # ["x", "o", "x", "o", " ", "o", " ", "o", "o"]
            (Coordinate(2, 4), 1, 3, False), # basic case
            # [" ", "o", "o", "o", " ", " ", " ", "x", "x"]
            (Coordinate(9, 4), 0, 3, False), # both side empty, return False
            # ["x", "o", "o", "o", " ", "o", " ", "x", "x"]
            (Coordinate(6, 4), 6, 8, True), # edge case
            (Coordinate(6, 4), 2, 5, True), # jump case
            # ["x", "o", "x", "o", " ", "o", " ", "o", "o"]
            (Coordinate(2, 4), 5, 8, True), # jump and edge case
        ])
    
        def test_is_single_side_empty(self, board, coordinate, left, right, expected_result):
            _line = RowLine(board, coordinate)
            assert GameAnalyzer._is_single_side_empty(_line, left, right) == expected_result    
    
    class TestIsBothSideEmpty:
        @pytest.fixture
        def board(self):
            return _create_test_board()
        
        # check window[left, right]'s side are empty
        @pytest.mark.parametrize("coordinate, left, right, expected_result", [
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "]
            (Coordinate(1, 4), 4, 7, False),
            # [" ", "o", "o", "o", " ", " ", " ", "x", "x"]
            (Coordinate(9, 4), 1, 4, True),
            (Coordinate(9, 4), 0, 3, True),
            # ["x", "o", "o", "o", " ", "o", " ", "x", "x"]
            (Coordinate(6, 4), 7, 8, False),
            (Coordinate(6, 4), 2, 5, False),
        ])
    
        def test_is_both_side_empty(self, board, coordinate, left, right, expected_result):
            _line = RowLine(board, coordinate)
            assert GameAnalyzer._is_both_side_empty(_line, left, right) == expected_result
    """
    
    class TestGetWindows:
        @pytest.fixture
        def board(self):
            return _create_test_board()
    
        @pytest.mark.parametrize("coordinate, mark, finding_length, expected_result", [
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "]
            (Coordinate(1, 4),"x", 4, [(2, 6), (3, 7)]),
            # ["x", "x", "x", "x", " ", "x", " ", "o", "o"]
            (Coordinate(3, 4), "x", 4, [(0, 4), (1, 5)]),
            # ["o", "o", "o", "o", "o", "o", "o", "o", "o"]
            # return None because we check finding_length + 1 size window
            (Coordinate(5, 4), "o", 4, []), 
            # [" ", "o", "o", "o", " ", " ", " ", "x", "x"]
            (Coordinate(9, 3), "o", 3, [(0, 3), (1, 4)]),
        ])

        def test_get_windows(self, board, coordinate, mark, finding_length, expected_result):
            _line = RowLine(board, coordinate)
            assert GameAnalyzer._get_windows(_line, mark, finding_length) == expected_result


    class TestGetLengthNoJump:
        @pytest.fixture
        def board(self):
            return _create_test_board()
            
        @pytest.mark.parametrize("coordinate, mark, expected_result", [
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "] basic length with o
            (Coordinate(1, 2), "o", 2),
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "] basic length with x
            (Coordinate(1, 4), "x", 4),
            # ["o", "o", "o", "o", "o", "o", "o", "o", "o"] basic length 9
            (Coordinate(5, 9), "o", 9),
            # ["x", "o", "o", "o", " ", "o", " ", "x", "x"] if 6,5 change to " ", length will be 3
            (Coordinate(6, 6), " ", 1),
            (Coordinate(6, 2), "o", 3),
            # [" ", "o", "o", "o", " ", "x", "x", "x", "x"] there is no "x" at position, return 1 
            (Coordinate(9, 1), " ", 1),
            # [" ", "o", "o", "o", " ", "x", "x", "x", "x"] 
            (Coordinate(9, 6), "x", 4),
        ])
        # index of marked coordinate is Coordinate[0] because using RowLine
        def test_get_length_no_jump(self, board, coordinate, mark, expected_result):
            _line = RowLine(board, coordinate)
            assert GameAnalyzer.get_length_of_chain(_line, mark) == expected_result

class TestRowLine:
    @pytest.fixture
    def board(self):
        return _create_test_board()

    @pytest.mark.parametrize("coordinate, expected_result", [
        (Coordinate(1,8), ["x", "o", "o", "x", "x", "x", "x", "o", " "]),
        (Coordinate(2,2), ["x", "o", "x", "o", " ", "o", " ", "o", "o"]),
        (Coordinate(6,1), ["x", "o", "o", "o", " ", "o", " ", "x", "x"]),
    ])
    def test_row_line(self, board, coordinate, expected_result):
        _row_line = RowLine(board, coordinate)
        assert _row_line.line == expected_result

    def test_row_line_invalid_coordinate(self, board):
        # Test with an invalid coordinate (not within board's range)
        invalid_coordinate = Coordinate(10, 1)
        with pytest.raises(IndexError):
            RowLine(board, invalid_coordinate)

class TestColumnLine:
    @pytest.fixture
    def board(self):
        return _create_test_board()

    @pytest.mark.parametrize("coordinate, expected_result", [
        (Coordinate(1,1), ["x", "x", "x", " ", "o", "x", "x", "o", " "]),
        (Coordinate(4,4), ["x", "o", "x", "o", "o", "o", "x", "o", "o"]),
        (Coordinate(8,9), [" ", "o", "o", "x", "o", "x", "x", "x", "x"]),
    ])
    def test_column_line(self, board, coordinate, expected_result):
        _column_line = ColumnLine(board, coordinate)
        assert _column_line.line == expected_result

    def test_column_line_invalid_coordinate(self, board):
        # Test with an invalid coordinate (not within board's range)
        invalid_coordinate = Coordinate(1, 10)
        with pytest.raises(IndexError):
            ColumnLine(board, invalid_coordinate)

class TestCrossLeftToRightLine:
    @pytest.fixture
    def board(self):
        return _create_test_board()

    @pytest.mark.parametrize("coordinate, expected_result", [
        (Coordinate(1,1), ["x", "o", "x", "o", "o", "o", "x", "x", "x"]),
        (Coordinate(1,7), ["x", "o", "o"]),
        (Coordinate(1,9), [" "]),
        (Coordinate(7,4), [" ", "o", "o", "x", "x", "x"]),
    ])
    def test_cross_left_to_right_line(self, board, coordinate, expected_result):
        _cross_line = PrincipalDiagonalLine(board, coordinate)
        assert _cross_line.line == expected_result

class TestCrossRightToLeftLine:
    @pytest.fixture
    def board(self):
        return _create_test_board()

    @pytest.mark.parametrize("coordinate, expected_result", [
        (Coordinate(1,1), ["x"]),
        (Coordinate(4,4), ["x", "o", " ", "o", "o", "o", "x"]),
        (Coordinate(1,9), [" ", "o", " ", "o", "o", "o", "x", "o", " "]),
        (Coordinate(9,6), ["x", "x", "x", "x"]),
    ])
    def test_cross_right_to_left_line(self, board, coordinate, expected_result):
        _cross_line = SecondaryDiagonalLine(board, coordinate)
        assert _cross_line.line == expected_result
