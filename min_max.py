from collections import deque
from typing import List, Tuple, Set, Dict
from board import Line, GameBoard, Coordinate, RowLine, ColumnLine, CrossLeftToRightLine, CrossRightToLeftLine
from game_rule import GameRule
from game_mark import GameMark
from player import Player
import copy

class MinMax():
    MAX_DEPTH = 2
        
    def find_best_move(self, board:GameBoard, player: Player, opponent_player: Player, depth=MAX_DEPTH):
        _mark = player.get_mark()
        
        best_score = float('-inf')
        best_move = None

        for _coordinate in self.get_simulate_moves(board):
            new_board = copy.deepcopy(board)
            new_board.set_mark(_coordinate, _mark)
            alpha = float("-inf")
            beta = float("inf")
            _score, _ = self.scoring(new_board, _coordinate, opponent_player,  player, alpha, beta, depth, False)

            if _score > best_score:
                best_score = _score
                best_move = _coordinate
        return (best_move.row, best_move.column)
        

    # return score for each simulated coordinate
    def scoring(self, board: GameBoard, move:Coordinate, player: Player, opponent_player: Player, alpha: int, beta:int, depth: int, my_turn=True) -> Tuple[int, Coordinate]:
        if depth == 0 or GameRule().is_over(board, move, player):
            return self.evaluate_move(board, move, player), None

        if my_turn:
            max_score = float('-inf')
            best_move = None
            _mark = player.get_mark()
            for _coordinate in self.get_simulate_moves(board):
                new_board = copy.deepcopy(board)
                new_board.set_mark(_coordinate, _mark)
                _score, _ = self.scoring(new_board, _coordinate, opponent_player, player, alpha, beta, depth - 1, False)
                if _score > max_score:
                    max_score = _score
                    best_move = _coordinate
                    
                alpha = max(alpha, _score)
                if beta <= alpha:
                    break
                
            return max_score, best_move
        else:
            min_score = float('inf')
            best_move = None
            _mark = opponent_player.get_mark()
            for _coordinate in self.get_simulate_moves(board):
                new_board = copy.deepcopy(board)
                new_board.set_mark(_coordinate, _mark)
                _score, _ = self.scoring(new_board, _coordinate, player, opponent_player, alpha, beta, depth - 1, True)
                if _score < min_score:
                    min_score = _score
                    best_move = _coordinate
                    
                beta = min(beta, _score)
                if beta <= alpha:
                    break
                
            return min_score, best_move

    # simulate move for each empty cell and return coordinate, game board
    def get_simulate_moves(self, board: GameBoard) -> List[Coordinate]:
        _coordinates = []
        for i in board.row_range():
            for j in board.column_range():
                if not board.is_empty(i, j):
                    continue
                _coordinates.append(Coordinate(i, j))
        return _coordinates

    # return +999 ~ -999 - assessed score of board when making move
    def evaluate_move(self, board: GameBoard, coordinate: Coordinate, player: Player) -> int:
        score = 0
        _rule = GameRule()
        if _rule.is_prohibited_move(board, coordinate, player):
            return 0
        
        if _rule.has_winner(board, coordinate):
            return 999
        
        score += self.evaluate_line(RowLine(board, coordinate))
        score += self.evaluate_line(ColumnLine(board, coordinate))
        score += self.evaluate_line(CrossLeftToRightLine(board, coordinate))
        score += self.evaluate_line(CrossRightToLeftLine(board, coordinate))
        return score

    def evaluate_line(self, line: Line) -> int:
        score = 1
        if line.has_chain4():
            score += 50
        if line.has_chain3():
            score += 50
        if line.has_chain2():
            score += 10
        return score



"""
    # check all empty cell and simulate if move is prohibited
    # return simulated prohibit moves
    def get_simulate_prohibited(self, board: GameBoard, player: Player) -> Set[Tuple[int, int]]:
        prohibited_set = set()
        for i in board.row_range():
            for j in board.column_range():
                
                if not board.is_empty(i, j):
                    continue
                
                _board = copy.deepcopy(board)
                _coordinate = Coordinate(i, j)
                _mark = player.get_mark()
                _board.set_mark(_coordinate, _mark)
                
                if GameRule().is_prohibited_move(_board, _coordinate, player):
                    prohibited_set.add((i, j))
        return prohibited_set

    def get_mark_exist_row_lines(self, board: GameBoard) -> Dict:
        _lines = {}
        for i in board.row_range():
            _coordinate = Coordinate(i, 1) # fake coordinate to get Line
            RowLine(board, _coordinate)
            if RowLine.is_line_empty():
                continue
            
            _lines[(i, 1)] = RowLine.line
        return _lines

    def get_mark_exist_column_lines(self, board: GameBoard) -> Dict:
        _lines = {}
        for i in board.column_range():
            _coordinate = Coordinate(1, i) # fake coordinate to get Line
            ColumnLine(board, _coordinate)
            if ColumnLine.is_line_empty():
                continue
            
            _lines[(1, i)] = ColumnLine.line
        return _lines

    def get_mark_exist_left_to_right_cross_lines(self, board: GameBoard) -> Dict:
        _lines = {}
        for i in board.row_range():
            # coordinate is the position of line from up-right edge to down-left edge
            _coordinate = Coordinate(i, board.column() + 1 - i) # fake coordinate to get Line
            CrossLeftToRightLine(board, _coordinate)
            # get lines longer than 5
            if CrossLeftToRightLine.is_line_empty() or len(CrossLeftToRightLine.line) < 5:
                continue
            _lines[(i, board.column() + 1 - i)] = CrossLeftToRightLine.line
        return _lines

    def get_mark_exist_right_to_left_cross_lines(self, board: GameBoard) -> Dict:
        _lines = {}
        for i in board.row_range():
            # coordinate is the position of line from up-left edge to down-right edge
            _coordinate = Coordinate(i, i) # fake coordinate to get Line
            CrossRightToLeftLine(board, _coordinate)
            # get lines longer than 5
            if CrossRightToLeftLine.is_line_empty() or len(CrossRightToLeftLine.line) < 5:
                continue
            _lines[(i, i)] = CrossRightToLeftLine.line
        return _lines
"""