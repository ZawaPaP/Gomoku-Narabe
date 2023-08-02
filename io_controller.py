import re
from typing import Tuple
from error import InvalidIntInputError, InvalidCoordinateError
from board import Coordinate

class InputOutput:
    @staticmethod
    def get_input(prompt: str) -> str:
        return input(prompt)

class IOController:
    @staticmethod
    def get_integer_input(prompt: str) -> int:
        while True:
            try:
                user_input = InputOutput.get_input(prompt)
                return int(user_input)
            except ValueError:
                raise InvalidIntInputError()

    @staticmethod
    def get_coordinate_input(prompt: str) -> Coordinate:
        while True:
            user_input = InputOutput.get_input(prompt)
            parsed_input = IOController.parse_input(user_input)
            if IOController.validate_input(parsed_input):
                coordinate = Coordinate(map(int, parsed_input.split(",")))
                if coordinate.is_in_board():
                    return coordinate

    @staticmethod
    def validate_input(input_str: str) -> bool:
        pattern = r"\d+,\d+"
        return re.match(pattern, input_str)

    @staticmethod
    def validate_input_range(user_input: int, input_range: range) -> bool:
        if user_input in input_range:
            return True
        return False

    @staticmethod
    def parse_input(input_str: str) -> str:
        input_str = input_str.replace(" ", "")
        return input_str
