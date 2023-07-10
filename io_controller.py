from console_io import ConsoleIO
import re
from typing import Tuple
class IOController:
    @staticmethod
    def get_input(prompt: str) -> str:
        return ConsoleIO.get_input(prompt)

    @staticmethod
    def get_integer_input(prompt: str) -> int:
        while True:
            try:
                user_input = ConsoleIO.get_input(prompt)
                value = int(user_input)
                return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def get_position_input(board, prompt) -> Tuple[int, int]:
        while True:
            user_input = ConsoleIO.get_input(prompt)
            parsed_input = IOController.parse_input(user_input)
            if IOController.validate_position_format(parsed_input):
                row, column = map(int, parsed_input.split(","))
                if IOController.validate_input_range_board(row, column, board):
                    return row, column
            else:
                raise ValueError("Invalid input. Try again.")

    @staticmethod
    def  validate_input_range_board(row, column, board) -> bool:
        if row in board.row_range() and column in board.column_range():
            return True
        else:
            raise ValueError(f"Invalid input. Enter integer in the {board.row_range()}.") from None

    @staticmethod
    def  validate_input_range(data: int, data_range: range) -> bool:
        if data in data_range:
            return True
        else:
            raise ValueError(f"Invalid input. Enter should be in the {data_range}.") from None


    @staticmethod
    def validate_position_format(input: str) -> bool:
        pattern = r"\d+,\d+"
        return re.match(pattern, input)

    @staticmethod
    def parse_input(input_str: str) -> str:
        try:
            input_str = input_str.replace(" ", "")
            return input_str
        except ValueError:
            raise ValueError("Invalid input. Try again")
