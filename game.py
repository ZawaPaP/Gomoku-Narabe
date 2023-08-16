from error import NotEmptyCoordinateError
from board import GameBoard, Coordinate
from board_renderer import ConsoleRenderer
from player_manager import PlayerManager
from game_rule import GameRule
from game_mode import GameMode
from game_analyzer import GameAnalyzer
from io_controller import IOController

class Game:
    def __init__(self) -> None:
        self.game_mode = self.select_mode()
        self.player_manager = PlayerManager(self.game_mode)
        self.board = GameBoard()
        self.rule = GameRule()

    def play(self):
        self.player_manager.set_players()
        self.display_initial_text()
        while True:
            try:
                player = self.player_manager.get_current_player()
                #print(f"{player.name}'s turn\n")
                #player.make_move(self.board) 
                coordinate = player.get_mark_coordinate(self.board)
                if self.board.is_coordinate_empty(coordinate):
                    self.board.set_mark(coordinate, player.mark)
                else:
                    raise NotEmptyCoordinateError()
                ConsoleRenderer.render(self.board)
                if self.rule.is_over(self.board, coordinate, player.mark, player.is_first_player()):
                    break
                
                self.player_manager.next_player()
                
            except ValueError or IndexError as e:
                print(str(e))
                continue
        if self.rule.prohibited_long_chain(self.board, coordinate, player.mark, player.is_first_player()): 
            print(f"prohibited move: over line length {coordinate.row, coordinate.column}")
            return
        if self.rule.is_win_move(self.board, coordinate, player.mark): 
            print(f"{player.get_name()} win - marked {coordinate.row, coordinate.column}")
            return
        
        if self.rule.prohibited_chain_by_chain(self.board, coordinate, player.mark, player.is_first_player(), GameAnalyzer.has_three_by_three): 
            print(f"prohibited move: three by three {coordinate.row, coordinate.column}")
            return
        if self.rule.prohibited_chain_by_chain(self.board, coordinate, player.mark, player.is_first_player(), GameAnalyzer.has_four_by_four): 
            print(f"prohibited move: four by four {coordinate.row, coordinate.column}")
            return
        if self.rule.is_draw(self.board):
            print(f"draw game - marked {coordinate.row, coordinate.column}")
            return

    def display_initial_text(self):
        print("TicTacToe Game START!\n")
        ConsoleRenderer.render(self.board)

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