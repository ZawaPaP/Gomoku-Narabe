import pytest
from board import GameBoard, Coordinate, RowLine, ColumnLine, CrossLeftToRightLine, CrossRightToLeftLine, Line
from player import Player, CPUPlayer
from player_manager import PlayerManager
from game_mode import GameMode
from min_max import MinMax


class Board(GameBoard):
    # create coordinate class simply
    def c(self, row, column):
        return Coordinate(row, column)
    
    # only use to create test board 
    def _set_line(self, row, marks):
        for index, mark in enumerate(marks):
            self.set_mark(self.c(row, index + 1), mark)

# example board for test
def _create_test_board_01():
    board = Board()
    board._set_line(1, ["o", "x", "o", " ", " ", "x", " ", "o", " "])
    board._set_line(2, [" ", "x", " ", "o", " ", "o", "x", "o", " "])
    board._set_line(3, [" ", "x", "o", " ", " ", " ", " ", "o", " "])
    board._set_line(4, [" ", "o", "o", " ", "o", " ", " ", "x", " "])
    board._set_line(5, [" ", "o", "x", "o", " ", " ", "o", "o", "x"])
    board._set_line(6, [" ", "x", "o", "x", " ", "o", " ", " ", " "])
    board._set_line(7, [" ", " ", " ", " ", "x", "o", " ", " ", " "])
    board._set_line(8, [" ", " ", " ", " ", " ", "o", " ", " ", " "])
    board._set_line(9, [" ", "x", "x", "x", " ", " ", " ", " ", " "])
    return board

# example board for test
def _create_test_board_02():
    board = Board()
    board._set_line(1, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(2, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(3, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(4, [" ", " ", " ", "o", "x", " ", " ", " ", " "])
    board._set_line(5, [" ", " ", " ", "o", " ", "x", " ", " ", " "])
    board._set_line(6, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(7, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(8, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(9, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    return board

class TestMinMax:
    
    class TestFindBestMove:
        @pytest.fixture
        def board(self):
            return _create_test_board_02()

        def test_find_best_move(self, board):
            player = CPUPlayer("test_cpu1", "x")
            player.order = 1
            opponent_player = CPUPlayer("test_cpu2", "o")
            opponent_player.order = 2
            assert MinMax().find_best_move(board, player, opponent_player) == (3, 4)

    class TestEvaluateMove:
        @pytest.fixture
        def board(self):
            return _create_test_board_01()

        @pytest.fixture
        def player(self):
            return CPUPlayer("test_cpu", "o")
        
        @pytest.mark.parametrize('coordinate, expected_result', [
            (Coordinate(1, 1), 4), 
            (Coordinate(4, 2), 104),
            (Coordinate(7, 6), 64),
            (Coordinate(3, 8), 4),
        ])

        def test_evaluate_move(self, board, coordinate, player, expected_result):
            assert MinMax().evaluate_move(board, coordinate, player) == expected_result  

    """
    class TestGetSimulatedProhibited:
        @pytest.fixture
        def board(self):
            return _create_test_board()

        @pytest.fixture
        def player(self):
            return CPUPlayer("test_cpu", "o")
        
        def test_get_simulate_prohibited(self, board, player):
            player.order = 1
            expected_result = (
                # safe case
                # (3,4)make 4x4 but 5chain prioritized
                # (3,5)make 3x3 but 5chain prioritized
                (1,1),   # over line
                (2,3),   # over line
                (2,5),   # 4x4 - jump x jump
                (2,7),   # 4x4 - jump x jump
                (4,1),   # 4x4 - jump x jump
                (4,2),   # overline
                (4,7),   # over line fill out blank
                (4,9),   # 4x4 with jumping overline
                (6,5),   # overline
                (6,8),   # 4x4
                (7,1),   # 4x4 no jump x no jump
                (7,4),   # 4x4 jump x no jump
                (7,5),   # 4x4 jump x no jump
                (7,7),   # overline
                (8,2),   # 4x4
                (8,4),   # 4x4
                (8,7),   # 3x3 - jump x no jump
                (9,1),   # 4x4
                (9,6),   # 4x4
                )
            result = MinMax().get_simulate_prohibited(board, player)
            assert sorted(result) == sorted(expected_result)

    class TestFindCheckPosition:
        @pytest.fixture
        def board(self):
            return _create_test_board()

        @pytest.mark.parametrize('marks, expected_result', [
            # move is marked index (range: 1 to len(marks))
            ([" ", "o", "o", "o", "o", " "], [1, 6]),    # basic test having check points
            (["o", "o", "o", " ", "o", " "], [4]),        # basic test having point between marks
            (["o", "o", "o", "o", " ", " "], [5]),        # basic test having point, edge case
            (["o", "o", "o", "o", " ", "o"], [5]),        # basic test having point, having longer marks
            ([" ", "o", "o", "o", " ", " "], []),        # basic test not having check
            (["o", "o", "o", "x", "o", " "], []),        # basic test not having check
        ])

        def test_find_check_position(self, board, marks, expected_result):
            coordinate = Coordinate(1,1) #fake coordinate
            _line = RowLine(board, coordinate)
            _line.line = marks
            assert MinMax().find_check_position(_line) == expected_result   
    """
