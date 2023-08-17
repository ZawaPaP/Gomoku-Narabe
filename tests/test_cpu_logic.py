import pytest
from board import GameBoard, Coordinate, RowLine, ColumnLine, PrincipalDiagonalLine, SecondaryDiagonalLine, Line
from player import Player, CPUPlayer
from player_manager import PlayerManager
from game_mode import GameMode
from cpu_logic import MinMax
from game_analyzer import GameAnalyzer

class Board(GameBoard):
    # create coordinate class simply
    def c(self, row, column):
        return Coordinate(row, column)
    
    # only use to create test board 
    def _set_line(self, row, marks):
        for index, mark in enumerate(marks):
            self.set_mark(self.c(row, index + 1), mark)

# example board for test
def _create_test_board_large_moves():
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
def _create_test_board_mid_moves():
    board = Board()
    board._set_line(1, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(2, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(3, [" ", " ", " ", "x", " ", " ", " ", " ", " "])
    board._set_line(4, [" ", " ", " ", "o", "x", " ", " ", " ", " "])
    board._set_line(5, [" ", " ", " ", "o", " ", "x", " ", " ", " "])
    board._set_line(6, [" ", " ", " ", "o", " ", " ", " ", " ", " "])
    board._set_line(7, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(8, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(9, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    return board

# example board for test
def _create_test_board_few_moves():
    board = Board()
    board._set_line(1, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(2, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(3, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(4, [" ", " ", " ", "o", "x", " ", " ", " ", " "])
    board._set_line(5, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(6, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(7, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(8, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    board._set_line(9, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
    return board

class TestMinMax:

    class TestGetRelevantCoordinates:
        @pytest.fixture
        def board(self):
            return _create_test_board_few_moves()

        def test_get_relevant_coordinates(self, board):
            tmp_list = []
            expected_result = [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 3), (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5), (5, 6), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]
            for coord in GameAnalyzer.get_marked_surroundings(board):
                tmp_list.append((coord.row, coord.column))
            assert sorted(tmp_list) == expected_result

    """
    class TestCalculateMoveScore:
        @pytest.fixture
        def board(self):
            return _create_test_board_large_moves()

        
        @pytest.mark.parametrize('coordinate, is_first_player, expected_result', [
            # ["o", "x", "o", " ", " ", "x", " ", "o", " "]
            (Coordinate(1, 1), True,  4), 
            # [" ", "o", "o", " ", "o", " ", " ", "x", " "]
            (Coordinate(4, 2), True, 104),
            # [" ", " ", " ", " ", "x", "o", " ", " ", " "]
            (Coordinate(7, 6), True, 64),
            # [" ", "x", "o", " ", " ", " ", " ", "o", " "]
            (Coordinate(3, 8), True, 4),
        ])

        def test_evaluate_move(self, board, coordinate, is_first_player, expected_result):
            player_mark = 'o'
            opponent_mark = 'x'
            assert MinMax().calculate_move_score(board, coordinate, player_mark, opponent_mark, is_first_player) == expected_result  


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
