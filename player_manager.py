from error import NoAvailableMarkError, PlayerManagerError
from player import Player, UserPlayer, CPUPlayer, PlayerType
from io_controller import IOController
from game_mark import GameMark
from game_mode import GameMode
from typing import List

class PlayerManager:
    def __init__(self, game_mode: GameMode) -> None:
        self.players = []
        self.game_mode = game_mode
        self.game_marks = GameMark.get_game_marks()
        self.number_of_user, self.number_of_cpu = GameMode.get_player_counts(game_mode)
        self.number_of_players = self.number_of_cpu + self.number_of_user
        self.get_current_player_index = 0
    
    def set_players(self) -> List[Player]:
        for i in range(self.number_of_user):
            name = f"{PlayerType.USER.name}_{i + 1}"
            mark = self.get_available_mark()    
            player = UserPlayer(name, mark)
            self.players.append(player)
        
        for i in range(self.number_of_cpu):
            name = f"{PlayerType.CPU.name}_{i + 1}"
            mark = self.get_available_mark()    
            player = CPUPlayer(name, mark)
            self.players.append(player)

        if self.game_mode == GameMode.PVC:
            if self.make_cpu_first_player():
                self.players.reverse()
        
        for player in self.players:
            player.order = self.players.index(player) + 1

    def get_current_player(self) -> Player:
        return self.players[self.get_current_player_index % self.number_of_players]

    def next_player(self):
        self.get_current_player_index += 1

    def get_opponent(self, player: Player) -> Player:
        if self.players != 2:
            raise PlayerManagerError()
        for _player in self.players:
            if player != _player:
                return _player

    def get_available_mark(self) -> str:
        try:
            return self.game_marks.pop(0)
        except IndexError:
            raise NoAvailableMarkError()

    @staticmethod
    def make_cpu_first_player() -> bool:
        while True:
            choice = IOController.get_integer_input(
                """
                Choose 1 for being the first player / Choose 2 for letting the CPU take the first turn.
                Please enter your choice: 
                """
            )
            if choice == 2:
                return True
            elif choice == 1:
                return False
            else:
                print("Invalid choice. Please enter either 1 or 2.")
