import signal, sys
from game_controller import GameController

def signal_handler(signal, frame):
    print("\nExit the program")
    sys.exit(0)


def main():
    GameController().start()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
