from game import Game
from io_controller import IOController

class GameController:
    def start(self):
        #while True:
            game = Game()
            game.play()
        #    if not self.ask_continue():
        #        break

    def ask_continue(self) -> bool:
        if self.is_confirmed_input("continue the new game? (y/n): "):
            return True
        return False

    @staticmethod
    def is_confirmed_input(text: str) -> bool:    
        confirmation = IOController.get_input(text)
        return confirmation.lower() == "y"
