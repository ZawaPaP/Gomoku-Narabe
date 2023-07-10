
from board import GameBoard
from board_renderer import GameBoardRenderer
from player_manager import PlayerManager
from game_rule import GameRule
from game_mode import GameMode
from io_controller import IOController

class Game:
    def __init__(self) -> None:
        self.game_mode = self.select_mode()
        self.player_manager = PlayerManager(self.game_mode)
        self.board = GameBoard()

    def play(self):
        self.player_manager.set_players()
        self.display_initial_text()
        while True:
            try:
                player = self.player_manager.get_current_player()
                print(f"{player.get_name()}'s turn\n")
                #player.make_move(self.board) 
                row, column = player.get_mark_position(self.board)
                if self.board.is_empty(row, column):
                    self.board.set_mark(row, column, player.get_mark())
                else:
                    raise ValueError("The position is already marked. Please choose an empty cell.")
                GameBoardRenderer(self.board).render()
                if GameRule.is_over(self.board):
                    break
                self.player_manager.move_to_next_player()
                
            except ValueError or IndexError as e:
                print(str(e))
                continue
            except Exception as e:
                print(f"Unexpected Error {e}")
                exit(1)

        if GameRule.has_winner(self.board): 
            print(f"{player.name} win")
            return
        elif GameRule.is_draw(self.board):
            print("draw game")
            return

    def display_initial_text(self):
        print("TicTacToe Game START!\n")
        GameBoardRenderer(self.board).render()

    def select_mode(self) -> GameMode:
        while True:
            try:
                game_mode = [str(mode.name) +": "+ str(mode.value) for mode in GameMode]
                user_input = IOController.get_integer_input(
                    str(game_mode) + "\n Select Game mode: "
                    )
                mode_range = range(1, len(GameMode) + 1)
                if IOController.validate_input_range(user_input, mode_range):
                    return GameMode(int(user_input))
            except ValueError as e:
                print(str(e))