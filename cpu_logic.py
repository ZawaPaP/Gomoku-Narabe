import logging
import random
import copy
from typing import List, Tuple
from board import Line, GameBoard, Coordinate
from game_rule import GameRule
from game_mark import GameMark
from game_analyzer import GameAnalyzer
import concurrent.futures
from abc import ABC, abstractmethod

logging.basicConfig(filename="minmax_metrics.log", level=logging.INFO)

class CPULogic(ABC):
    def __init__(self, player):
        self.player = player
    
    @abstractmethod
    def generate_move(self, board: GameBoard) -> Coordinate:
        pass

class DumbCPULogic(CPULogic):
    def __init__(self, player):
        super().__init__(player)
    
    def generate_move(self, board: GameBoard) -> Coordinate:
        while True:
            row = random.choice(board.row_range())
            column = random.choice(board.column_range())
            if not board.is_cell_empty(row, column):
                continue

            coordinate = Coordinate(row, column)
            board.set_mark(coordinate, self.player.mark)
            if GameRule().is_prohibited_move(board, coordinate, self.player.mark, self.player.is_first_player()):
                board.remove_mark(coordinate)
                continue
            board.remove_mark(coordinate)
            return coordinate

class HighCPULogic(CPULogic):
    def __init__(self, player):
        super().__init__(player)

    def generate_move(self, board: GameBoard) -> Coordinate:
        row, column =  MinMax().find_best_move(board, self.player.mark, self.player.opponent_mark() , self.player.is_first_player())
        return Coordinate(row, column)

class MinMax():
    MAX_DEPTH = 3
    TIME_LIMIT = 30
    WIN_SCORE = 9999
    CHAIN4x4_SCORE = 300
    CHAIN4x3_SCORE = 250
    CHAIN3x3_SCORE = 200
    CHAIN4_WITH_JUMP_SCORE = 75
    CHAIN4_NO_JUMP_SCORE = 100
    CHAIN3_WITH_JUMP_SCORE = 25
    CHAIN3_NO_JUMP_SCORE = 50
    CHAIN2_SCORE = 15
    CENTER_SCORE = 25
    BLOCK_CHAIN4 = 500
    BLOCK_CHAIN3 = 75
    HAS_POTENTIAL5 = 2
    
    def __init__(self):
        self.rule = GameRule()
        self.search_queue = None
        self.searched_set = None
        
    def log_depth(self, depth:int):
        logging.info(f"MinMax depth: {depth}")

    def get_future_results(self, board, search_area, player_mark, opponent_mark, is_first_player, alpha, beta, depth):
        args = [(board, coordinate, player_mark, opponent_mark, is_first_player, alpha, beta, depth, True) for coordinate in search_area]
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            results = {}
            try:
                for result, coordinate in zip(executor.map(self.min_max_search, *zip(*args)), search_area):
                    score, _ = result
                    results[coordinate] = score
            except Exception as e:
                print(f'Exception during processing: {e}')
            return results

    def find_best_move(self, board:GameBoard, player_mark: GameMark, opponent_mark: GameMark, is_first_player: bool, depth=MAX_DEPTH):
        # check limit time of minmax search
        # start_time = time.time()
        if board.is_empty():
            return ((board.row() + 1 )// 2, (board.column() + 1) // 2)
        
        best_score = float('-inf')
        best_move = None
        
        search_area = self.get_search_areas(board, player_mark, opponent_mark, is_first_player)
        results = self.get_future_results(board, search_area, player_mark, opponent_mark, is_first_player, float('-inf'), float('inf'), depth)
        
        for coordinate, score in results.items():
            if score > best_score:
                best_score = score
                best_move = coordinate
        return (best_move.row, best_move.column)
    
        # return score for each simulated coordinate
    def min_max_search(self, board: GameBoard, move:Coordinate, player_mark: GameMark, opponent_mark: GameMark, is_first_player: bool, alpha: int, beta:int, depth: int, my_turn=True) -> Tuple[int, Coordinate]:
        if depth == 0 or self.rule.is_over(board, move, player_mark, is_first_player):
            return self.calculate_move_score(board, move, player_mark, opponent_mark, is_first_player), None
        if my_turn:
            return self.maximize(board, player_mark, opponent_mark, is_first_player, alpha, beta, depth)
        else:
            return self.minimize(board, player_mark, opponent_mark, is_first_player, alpha, beta, depth)

    """
    def _min_max_search_wrapper(self, args):
        board, move, player_mark, opponent_mark, is_first_player, alpha, beta, depth, my_turn = args
        board_clone = copy.deepcopy(board)
        if my_turn:
            board_clone.set_mark(move, opponent_mark) 
        else:
            board_clone.set_mark(move, player_mark) 
        result = self.min_max_search(board_clone, move, player_mark, opponent_mark, is_first_player, alpha, beta, depth, my_turn)
        return result
    """

    def maximize(self, board: GameBoard, player_mark: GameMark, opponent_mark: GameMark, is_first_player: bool, alpha: int, beta: int, depth: int) -> Tuple[int, int]:
        max_score = float('-inf')
        best_move = None
        search_area = self.get_search_areas(board, player_mark, opponent_mark, is_first_player)
        for coordinate in search_area:
            board.set_mark(coordinate, player_mark)
            _score, _ = self.min_max_search(board, coordinate, player_mark, opponent_mark, is_first_player, alpha, beta, depth - 1, False)
            board.remove_mark(coordinate)
        
            if _score > max_score:
                max_score = _score
                best_move = coordinate
            
            alpha = max(alpha, _score)
            if beta <= alpha:
                break

            if max_score == MinMax.WIN_SCORE:
                break
        return max_score, best_move
        
    def minimize(self, board: GameBoard, player_mark: GameMark, opponent_mark: GameMark, is_first_player: bool, alpha: int, beta: int, depth: int) -> Tuple[int, int]:
        min_score = float('inf')
        best_move = None
        search_area = self.get_search_areas(board, player_mark, opponent_mark, is_first_player)
        
        for coordinate in search_area:
            board.set_mark(coordinate, opponent_mark)
            _score, _ = self.min_max_search(board, coordinate, player_mark, opponent_mark, is_first_player, alpha, beta, depth - 1, True)
            board.remove_mark(coordinate)
            
            if _score < min_score:
                min_score = _score
                best_move = coordinate
            beta = min(beta, _score)
            if beta <= alpha:
                break
        return min_score, best_move
        

    def calculate_move_score(self, board: GameBoard, coordinate: Coordinate, player_mark: GameMark, opponent_mark: GameMark, is_first_player: bool) -> int:
        _score = 0
        if self.rule.is_prohibited_move(board, coordinate, player_mark, is_first_player):
            return 0
        
        if self.rule.is_win_move(board, coordinate, player_mark):
            return self.WIN_SCORE
        
        _lines = board.get_lines_from_coordinate(coordinate)
        _score += self.evaluate_chain_of_lines(_lines, player_mark)
        _score += self.evaluate_blocking(board, coordinate, opponent_mark, is_first_player)
        _score += self.evaluate_centering(board, coordinate)
        return _score


    def evaluate_chain_of_lines(self, lines: List[Line], mark: GameMark) -> int:
        _score = 0
        
        for line in lines:
            if not GameAnalyzer.has_potential_for_chain5(line, mark):
                continue
            _score += self.HAS_POTENTIAL5
            _score += self.evaluate_individual_chain(line, mark)
        
        _score += self.evaluate_chain_combinations(lines, mark)
        return _score


    def evaluate_individual_chain(self, line: Line, mark: GameMark) -> int:
        _score = 0
        if GameAnalyzer.has_chain4_with_jump(line, mark):
            _score += self.CHAIN4_WITH_JUMP_SCORE
        if GameAnalyzer.has_chain4_without_jump(line, mark):
            _score += self.CHAIN4_NO_JUMP_SCORE
        if GameAnalyzer.has_chain3_with_jump(line, mark):
            _score += self.CHAIN3_WITH_JUMP_SCORE
        if GameAnalyzer.has_chain3_without_jump(line, mark):
            _score += self.CHAIN3_NO_JUMP_SCORE
        if GameAnalyzer.has_chain2(line, mark):
            _score += self.CHAIN2_SCORE
        return _score

    def evaluate_chain_combinations(self, lines: List[Line], mark: GameMark) -> int:
        chain4_count = sum(1 for line in lines if GameAnalyzer.has_chain4(line, mark))
        chain3_count = sum(1 for line in lines if GameAnalyzer.has_chain3(line, mark))

        _score = 0
        if chain4_count >= 2:
            _score += self.CHAIN4x4_SCORE
        if chain3_count >= 2:
            _score += self.CHAIN3x3_SCORE
        if chain4_count >= 1 and chain3_count >= 1:
            _score += self.CHAIN4x3_SCORE
        return _score


    def evaluate_blocking(self, board:GameBoard, coordinate: Coordinate, opponent_mark: GameMark, is_first_player: bool) -> int:
        _original_mark = board.get_mark(coordinate.row, coordinate.column)
        board.set_mark(coordinate, opponent_mark)
        _lines = board.get_lines_from_coordinate(coordinate)
        
        _score = 0
        if self.rule.is_prohibited_move(board, coordinate, opponent_mark, is_first_player):
            return _score
        
        for line in _lines:
            if not GameAnalyzer.has_potential_for_chain5(line, opponent_mark):
                continue
            if GameAnalyzer.has_chain4(line, opponent_mark):
                _score += self.BLOCK_CHAIN4
            if GameAnalyzer.has_chain3(line, opponent_mark):
                _score += self.BLOCK_CHAIN3
        board.set_mark(coordinate, _original_mark)
        return _score


    def evaluate_centering(self, board: GameBoard, coordinate: Coordinate) -> int:
        _center_row, _center_column = (board.row() + 1) // 2, (board.column() + 1) // 2
        return self.CENTER_SCORE - (abs(coordinate.row - _center_row) * abs(coordinate.column - _center_column))


    def get_search_areas(self, board: GameBoard, player_mark: GameMark, opponent_mark: GameMark, is_first_player: bool) -> List[Coordinate]:
        data = []        
        surroundings_list = list(GameAnalyzer.get_marked_surroundings(board, distance = 2))
        for coordinate in surroundings_list:
            board.set_mark(coordinate, player_mark)
            _score = self.calculate_move_score(board, coordinate, player_mark, opponent_mark, is_first_player)
            data.append((_score, coordinate))
            board.remove_mark(coordinate)

        sorted_data = sorted(data, key=lambda x: x[0], reverse=True)
        coordinates = [item[1] for item in sorted_data]
        return coordinates
