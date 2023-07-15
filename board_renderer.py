class Renderer:
    def render(self) -> None:
        raise NotImplementedError
        
    def get_row_number_list(self) -> None:
        raise NotImplementedError

    def get_column_number_list(self) -> None:
        raise NotImplementedError

class ConsoleRenderer(Renderer):
    def render(board) -> None:
        row_index = ConsoleRenderer.get_row_number_list(board)
        
        for i in board.row_range():
            if i == 1:
                print("  ", end="")
                [print(f" {row}  ",end ='') for row in row_index]
                print("\n")
            for j in board.column_range():
                if j == 1:
                    print(f"{i} ", end ='')
                if j != board.column():
                    print(f" {board.get_mark(i, j)} ", end = '|')
                else:
                    print(f" {board.get_mark(i, j)} ")
            if i != board.row():
                for k in board.column_range():
                    if k == 1:
                        print("  ---", end = '+')
                    elif k != board.column():
                        print("---", end = '+')
                    else:
                        print('---')
        print("\n")

    def get_row_number_list(board) -> None:
        return list(board.row_range())

    def get_column_number_list(board) -> None:
        return list(board.column_range())
