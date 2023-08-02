import signal, sys
import os, logging

from game_controller import GameController

def signal_handler(signal, frame):
    print("\nExit the program")
    sys.exit(0)


def main():
    if os.environ.get("DEBUG", 0):
        logging.basicConfig(level=logging.DEBUG)

    GameController().start()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
