from typing import List
from enum import Enum
class GameMark(Enum):
    EMPTY = ' '
    FIRST_USER = 'o'
    SECOND_USER = 'x'

    @classmethod
    def get_game_marks(cls) -> List[str]:
        marks = [mark.value for mark in GameMark]
        marks.remove(GameMark.EMPTY.value) # Remove the EMPTY mark from the list
        return marks

