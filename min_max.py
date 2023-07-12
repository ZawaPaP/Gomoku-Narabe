from collections import deque
from game_rule import GameRule
from board import GameBoard
from board_renderer import Renderer
from typing import List
import math
import copy

class TreeNode():
    def __init__(self, value = None):
        self.value = value
        self.children = []
        
    def add_child(self, child_node_value):
        node = TreeNode(child_node_value)
        self.children.append(node)

    def get_value(self):
        return self.value

    def get_children(self):
        return self.children

class MinMax():

    def min_max(self, board, mark):
        root = TreeNode(board)
        #empty_cell_list
        empty_list = self.get_board_empty_list(board)
        #純関数にしたほうがよい
        self.create_move_tree(board, root, mark)
        #純関数にしたほうがよい
        self.return_child_node_win_lose_value(root)

        print([child.get_value() for child in root.children])
        child_node_value = [child.get_value() for child in root.children]
        i = child_node_value.index(max(child_node_value)) # boardにおいてemptyな場所のi番目
        return empty_list[i]

    def create_move_tree(self, board, tree, mark):
        if GameRule.is_over(board):
            return
        else:
            for i in board.row_range():
                for j in board.column_range():
                    if board.is_empty(i, j):
                        next_board = copy.deepcopy(board)
                        next_board.set_mark(i, j, mark)
                        tree.add_child(next_board)
                        next_mark = 'x' if mark == 'o' else 'o'
                        self.create_move_tree(next_board, tree.children[-1], next_mark)

    # 自分ターンの場合、子ノードの最大値、哀帝ターンの場合、子ノードの最小値を返す
    def return_child_node_win_lose_value(self, node, turn = 0):  #node.value = board
        if not node.get_children():
            #node.value = board
            if GameRule.has_winner(node.value):
                if turn % 2 == 1:
                    node.value = 1
                else:
                    node.value = -1
            elif GameRule.is_draw(node.value):
                node.value = 0
            else:
                print("Unexpected error")
                exit()
            return node.value
        elif turn % 2 == 0: #自分のターン
            turn += 1
            tmp = 0
            for child in node.children:
                tmp += self.return_child_node_win_lose_value(child, turn)
            node.value = tmp
            return tmp
        else: #相手のターン
            turn += 1
            tmp = 0 
            for child in node.children:
                tmp += self.return_child_node_win_lose_value(child, turn)
            node.value = tmp
            return tmp

    def get_board_empty_list(self, board) -> List[tuple]:
        empty_list = []
        for i in board.row_range():
            for j in board.column_range():
                if board.is_empty(i, j):
                    empty_list.append((i, j))
        return empty_list

    '''
    # 自分ターンの場合、子ノードの最大値、哀帝ターンの場合、子ノードの最小値を返す
    def __return_child_node_max_value(self, node, turn = 2):
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
        self.__return_child_node_max_value(node)
        self.breath_first_search(node)

root = TreeNode(0)
root.add_child(1)
root.add_child(2)
root.add_child(3)
root.children[0].add_child(4)
root.children[0].children[0].add_child(8)
root.children[0].children[0].add_child(10)
root.children[0].children[0].children[0].add_child(11)
root.children[0].add_child(9)
root.children[2].add_child(5)
root.children[2].children[0].add_child(6)
root.children[2].children[0].add_child(7)
'''

#board = GameBoard()
#root = TreeNode(board)
#MinMax().create_move_tree(board, root)
#MinMax().return_child_node_win_lose_value(root)
#print([child.get_value() for child in root.children])
#MinMax().breath_first_search(root)