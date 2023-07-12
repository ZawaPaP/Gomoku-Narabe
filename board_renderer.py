class Renderer:
    def __init__(self, board) -> None:
        self.board = board
        
class ConsoleRenderer(Renderer):
    def __init__(self, board) -> None:
        super().__init__(board)
    
    def render(self) -> None:
        for i in self.board.row_range():
            for j in self.board.column_range():
                if j != self.board.column():
                    print(f" {self.board.get_mark(i, j)} ", end = '|')
                else:
                    print(f" {self.board.get_mark(i, j)} ")
            if i != self.board.row():
                for k in self.board.column_range():
                    if k != self.board.column():
                        print("---", end = '+')
                    else:
                        print('---')
        print("\n")
