from enum import Enum
from typing import Tuple
class GameMode(Enum):
    PVP = 1
    PVC = 2
    CVC = 3

    @classmethod
    def get_player_counts(cls, game_mode: "GameMode") -> Tuple["number_of_user":int, "number_of_cpu": int]:
        if game_mode == cls.CVC:
            return 0, 2  # 0 players, 2 CPUs
        elif game_mode == cls.PVC:
            return 1, 1  # 1 player, 1 CPU
        elif game_mode == cls.PVP:
            return 2, 0  # 2 players, 0 CPUs
        else:
            raise ValueError("Invalid game mode")
