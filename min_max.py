from collections import deque
from typing import List, Tuple, Set
from board import Line, GameBoard, Coordinate, CrossRightToLeftLine
from game_rule import GameRule
from player import Player
import math
import copy

class MinMax():
    def breath_first_search(self, root):
        Deque = deque([root])
        while len(Deque) > 0:
            node = Deque.popleft()
            if node is not None:
                print(node.value)
                
                for child in node.children:
                    Deque.append(child)

    # return child node max value
    def test(self, node):
        self.breath_first_search(node)
        self.return_child_node_max_value(node)
        self.breath_first_search(node)

    # 自分ターンの場合、子ノードの最大値、相手ターンの場合、子ノードの最小値を返す
    def return_child_node_max_value(self, node, turn = 2):
        if not node.children:
            # node.value ではなく静的評価関数をかえす
            return node.value
        elif turn % 2 == 1:
            turn -= 1
            tmp = - math.inf
            for child in node.children:
                tmp = max(tmp, self.return_child_node_max_value(child, turn))
            node.value = tmp
            return tmp
        elif turn % 2 == 0:
            turn -= 1
            tmp = math.inf
            for child in node.children:
                tmp = min(tmp, self.return_child_node_max_value(child, turn))
            node.value = tmp
            return tmp

    def scoring_line(self, line: Line) -> List[int]:
        if line.is_line_empty():
            return [0] * len(line)
        
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

    # check if 
    def find_check_position(self, line: Line, player: Player) -> List[int]:
        if line.is_line_empty():
            return None
        
        result = []
        _mark = player.get_mark()
        # +1 due to return coordinate of the board (1 ~ 9)
        for i in range(1, len(line.line) + 1):
            if line.is_marked_position(i):
                continue
            line.index = i
            if line.get_length_without_jump(_mark) >= 5:
                result.append(i)
        return result

