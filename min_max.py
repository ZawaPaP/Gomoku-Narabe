from collections import deque
import math

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

    # 自分ターンの場合、子ノードの最大値、哀帝ターンの場合、子ノードの最小値を返す
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





class TreeNode():
    def __init__(self, value):
        self.value = value
        self.children = []
        
    def add_child(self, child_node_value):
        # creates parent-child relationship
        node = TreeNode(child_node_value)
        self.children.append(node)

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

MinMax().test(root)