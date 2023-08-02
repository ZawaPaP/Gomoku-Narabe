import pytest
from error import NoOutCastMarkError
from board import GameBoard, Coordinate, RowLine, ColumnLine, CrossLeftToRightLine, CrossRightToLeftLine, Line
from game_mark import GameMark
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

class TestLine:

    class TestHasChain3:
        @pytest.fixture
        def board(self):
            return _create_test_board()

        @pytest.mark.parametrize('move, marks, expected_result', [
            # move is marked index (range: 1 to len(marks))
            (2, [" ", "o", "o", "o", " ", " "], True),     # basic chain3 without jump
            (2, [" ", "o", "o", " ", " ", " "], False),    # no chain 3
            (2, [" ", "o", "o", "x", "o", " "], False),    # no chain 3
            (2, ["o", "o", "o", " ", " ", " "], False),    # chain3 but only one-side empty, edge
            (2, ["x", "o", "o", "o", " ", " "], False),    # chain3 but only one-side empty, marked
            (2, ["o", "o", "o", "x", " ", " "], False),    # chain3 but not both-side empty, edge and marked
            (2, ["x", "o", "o", "o", "x", " "], False),    # chain3 but not both-side empty, marked
            (2, [" ", "o", "o", " ", "o", " "], True),     # chain3 with jump
            (2, [" ", "o", "o", " ", "o", "x"], False),    # chain3 with jump but only one-side empty, one side other mark
            (3, ["o", " ", "o", "o", " ", " "], False),    # chain3 with jump but only one-side empty, one side edge
            (3, ["o", "o", "o", "o", " ", " "], False),    # having chain4, one side empty
            (3, [" ", "o", "o", "o", "o", " "], False),    # having chain4, both side empty
            (3, ["x", "o", "o", "o", "o", "x"], False),    # having chain4, both side filled
            (3, [" ", "o", "o", "o", " ", "o"], False),    # having chain4 with jump
            (3, ["o", "o", "o", "o", "o", "o"], False),    # having chain4+
            (3, ["o", "o", "x", "o", "o", "o"], False),    # having chain4+
        ])

        def test_has_chain3(self, board, move, marks, expected_result):
            coordinate = Coordinate(1,1) #fake coordinate
            _line = RowLine(board, coordinate)
            _line.line = marks
            _line.index = move
            assert _line.has_chain3() == expected_result   


    class TestHasChain4:
        @pytest.fixture
        def board(self):
            return _create_test_board()
        
        @pytest.mark.parametrize('move, marks, expected_result', [
            # move is marked index (range: 1 to len(marks))
            (2, [" ", "o", "o", "o", "o", " "], True),     # basic chain4 without jump
            (2, [" ", "o", "o", "o", " ", " "], False),    # not having chain 4
            (2, [" ", "o", "o", "x", "o", "o"], False),    # not having chain 4
            (3, ["o", "o", "x", "o", "o", "o"], False),    # not having chain 4
            (2, ["o", "o", "o", "o", " ", " "], True),    # chain4, one-side empty
            (2, [" ", "o", "o", "o", " ", "o"], True),    # chain4 with jump
            (2, ["o", "o", "o", "o", "x", " "], False),    # chain4 but neither side empty
            (2, ["o", "o", "o", "o"], False),    # chain4 but neither side empty, edge
            (3, ["o", "o", "o", "o", "o", " "], False),    # having chain5
            (3, ["o", " ", "o", "o", "o", "o"], True),    # having chain5, with jump
            (3, ["x", "o", "o", "o", "o", "o", "x"], False),    # having chain5, neither sides empty
            (3, ["o", "o", "o", "o", "o", "o"], False),    # having chain4+
        ])
    
        def test_has_chain4(self, board, move, marks, expected_result):
            coordinate = Coordinate(1,1) #fake coordinate
            _line = RowLine(board, coordinate)
            _line.line = marks
            _line.index = move
            assert _line.has_chain4() == expected_result    

    class TestIsSingleSideEmpty:
        @pytest.fixture
        def board(self):
            return _create_test_board()
        
        # check window[left, right]'s side are empty
        @pytest.mark.parametrize("coordinate, left, right, expected_result", [
            # ["x", "o", "x", "o", " ", "o", " ", "o", "o"]
            (Coordinate(2, 4), 2, 4, False), # basic case
            # [" ", "o", "o", "o", " ", " ", " ", "x", "x"]
            (Coordinate(9, 4), 1, 4, True), # basic case
            # ["x", "o", "o", "o", " ", "o", " ", "x", "x"]
            (Coordinate(6, 4), 7, 9, True), # edge case
            (Coordinate(6, 4), 3, 6, True), # jump case
            # ["x", "o", "x", "o", " ", "o", " ", "o", "o"]
            (Coordinate(2, 4), 6, 9, True), # jump and edge case
        ])
    
        def test_is_single_side_empty(self, board, coordinate, left, right, expected_result):
            _line = RowLine(board, coordinate)
            assert _line._is_single_side_empty(left, right) == expected_result    
    
        def test_no_outcast_in_window(self, board):
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "]
            coordinate = Coordinate(1, 4)
            with pytest.raises(NoOutCastMarkError):
                RowLine(board, coordinate)._is_single_side_empty(4, 7)
    
    class TestIsBothSideEmpty:
        @pytest.fixture
        def board(self):
            return _create_test_board()
        
        # check window[left, right]'s side are empty
        @pytest.mark.parametrize("coordinate, left, right, expected_result", [
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "]
            (Coordinate(1, 4), 4, 7, False),
            # [" ", "o", "o", "o", " ", " ", " ", "x", "x"]
            (Coordinate(9, 4), 2, 5, True),
            (Coordinate(9, 4), 1, 4, True),
            # ["x", "o", "o", "o", " ", "o", " ", "x", "x"]
            (Coordinate(6, 4), 8, 9, False),
            (Coordinate(6, 4), 3, 6, False),
        ])
    
        def test_is_both_side_empty(self, board, coordinate, left, right, expected_result):
            _line = RowLine(board, coordinate)
            assert _line._is_both_side_empty(left, right) == expected_result
    
    
    class TestGetWindows:
        @pytest.fixture
        def board(self):
            return _create_test_board()
    
        @pytest.mark.parametrize("coordinate, finding_length, expected_result", [
            # ["x", "o", "o", "x", "x", "x", "x", "o", " "]
            (Coordinate(1, 4), 4, [(4, 8), (3, 7)]),
            # ["x", "x", "x", "x", " ", "x", " ", "o", "o"]
            (Coordinate(3, 4), 4, [(2, 6), (1, 5)]),
            # ["o", "o", "o", "o", "o", "o", "o", "o", "o"]
            # return None because we check finding_length + 1 size window
            (Coordinate(5, 4), 4, []), 
            # [" ", "o", "o", "o", " ", " ", " ", "x", "x"]
            (Coordinate(9, 3), 3, [(2, 5), (1, 4)]),
        ])

        def test_get_windows(self, board, coordinate, finding_length, expected_result):
            _line = RowLine(board, coordinate)
            assert _line._get_windows(finding_length) == expected_result


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
            (Coordinate(6, 6), " ", 3),
            # [" ", "o", "o", "o", " ", "x", "x", "x", "x"] there is no "x" at position, return 1 
            (Coordinate(9, 1), "x", 1),
            # [" ", "o", "o", "o", " ", "x", "x", "x", "x"] 
            (Coordinate(9, 5), "x", 5),
        ])
        # index of marked coordinate is Coordinate[0] because using RowLine
        def test_get_length_no_jump(self, board, coordinate, mark, expected_result):
            _line = RowLine(board, coordinate)
            assert _line.get_length_without_jump(mark) == expected_result


    class TestOutCastMarkIndex:
        @pytest.fixture
        def board(self):
            return _create_test_board()
            
        @pytest.mark.parametrize("data, coordinate, expected_result", [
            (["x", "o", "o", "o"], Coordinate(2, 1), 0),        # basic outcast finding
            (["x", "o", "x", "x", "x"], Coordinate(1, 3), 1),   # basic outcast finding
            ([" ", "o", "o", "o"], Coordinate(2, 2), 0),        # basic outcast finding with blank
        ])
        # index of marked coordinate is Coordinate[0] because using RowLine
        def test_outcast_mark_index_line(self, board, coordinate, data, expected_result):
            _line = RowLine(board, coordinate)
            assert _line._outcast_mark_index(data) == expected_result

        def test_outcast_mark_index_line(self, board):
            coordinate = Coordinate(5, 1)
            data = ["o", "o", "o", "o"]
            with pytest.raises(NoOutCastMarkError):
                RowLine(board, coordinate)._outcast_mark_index(data)


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
        _cross_line = CrossLeftToRightLine(board, coordinate)
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
        _cross_line = CrossRightToLeftLine(board, coordinate)
        assert _cross_line.line == expected_result
