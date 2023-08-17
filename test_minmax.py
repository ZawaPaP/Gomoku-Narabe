import time
import logging
from memory_profiler import memory_usage
from board import GameBoard
from game_mark import GameMark
from game_rule import GameRule
from game_analyzer import GameAnalyzer
from player_manager import PlayerManager
from cpu_logic import HighCPULogic
from game_mode import GameMode
from board_renderer import ConsoleRenderer

def measure_time(func):
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            memo_before = memory_usage()[0]
            result = func(*args, **kwargs)
            end_time = time.time()
            mem_after = memory_usage()[0]
        
            execution_time = end_time - start_time
            mem_usage = mem_after - memo_before
            logging.info(f"Function {func.__name__}: Execution time = {execution_time} seconds, Memory usage = {mem_usage} MB")
            
            return result
        except Exception as e:
            logging.error("Error in measure_time")
            raise e
    return wrapper

HighCPULogic.generate_move = measure_time(HighCPULogic.generate_move)

def game_example():
    board = GameBoard()
    player_manager = PlayerManager(GameMode.CVC)
    player_manager.set_players()
    rule = GameRule()
    logging.error(f"\n Start the game")
    while True:
        try:
            player = player_manager.get_current_player()
            coordinate = player.get_mark_coordinate(board)
            if board.is_coordinate_empty(coordinate):
                board.set_mark(coordinate, player.mark)
                logging.info(f"board marked {coordinate.row, coordinate.column} - {player.mark}")  
                ConsoleRenderer.render(board)
            else:
                continue
            if rule.is_over(board, coordinate, player.mark, player.is_first_player()):
                break
            
            player_manager.next_player()
            
        except ValueError or IndexError as e:
            print(str(e))
            continue
    if rule.prohibited_long_chain(board, coordinate, player.mark, player.is_first_player()): 
        logging.info(f"prohibited move: over line length {coordinate.row, coordinate.column}")
        return
    if rule.is_win_move(board, coordinate, player.mark): 
        logging.info(f"{player.get_name()} win - marked {coordinate.row, coordinate.column}")
        return
    if rule.prohibited_chain_by_chain(board, coordinate, player.mark, player.is_first_player(), GameAnalyzer.has_three_by_three): 
        logging.info(f"prohibited move: three by three {coordinate.row, coordinate.column}")
        return
    if rule.prohibited_chain_by_chain(board, coordinate, player.mark, player.is_first_player(), GameAnalyzer.has_four_by_four): 
        logging.info(f"prohibited move: four by four {coordinate.row, coordinate.column}")
        return
    if rule.is_draw(board):
        logging.info(f"draw game - marked {coordinate.row, coordinate.column}")
        return
        


# 4. テストの実行
if __name__ == "__main__":
    logging.basicConfig(filename="minmax_metrics.log", level=logging.INFO)
    game_example()