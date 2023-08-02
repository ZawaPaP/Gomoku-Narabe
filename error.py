
class GameSettingError(Exception):
    def __str__(self):
        return f"GameSettingError:"

class NoAvailableMarkError(GameSettingError):
    def __str__(self):
        return f"NoAvailableMarkError: there is no available mark."

class NoOutCastMarkError(GameSettingError):
    def __str__(self):
        return f"NoOutCastMarkError: there is no outcast mark in the window"


class InvalidInputError(Exception):

    def __str__(self):
        return f"InvalidInputError:"

class InvalidIntInputError(InvalidInputError):
    def __str__(self):
        return "Invalid input. Please enter a integer."


class InvalidInputParseError(InvalidInputError):
    def __str__(self):
        return "ParseError: Please input again."


class InvalidLineError(Exception):
    def __str__(self) -> str:
        return f"Invalid Line Error"

class NoLineExistError(InvalidLineError):
    def __str__(self) -> str:
        return "No line existing error"


class InvalidCoordinateError(Exception):
    def __str__(self):
        return f"InvalidCoordinateError:"
    
class OutRangeCoordinateError(InvalidCoordinateError):
    def __str__(self):
        return f"Coordinate is out of the board. {self.message}"

class NotEmptyCoordinateError(InvalidCoordinateError):
    def __str__(self):
        return "The position is already marked. Please choose an empty."









