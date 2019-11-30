from enum import Enum
class State(Enum):
    GAME_BEGIN = 0 # We do not know the number or type of players
    ROUND_BEGIN = 1 # Round begins
    ROUND_CONT = 2 # It is some player's turn
    ROUND_END = 3 # Round ends
    GAME_END = 4 # Game ends

class Prompt(Enum):
    NUM_PLAYERS = 0 # number of players
    FD = 1 # Player action draw/fold, cannot play
    PF = 2 # Player action play/fold, cannot draw

class GameErrors(Enum):
    GAME_FULL = 0 # Game is Full
    INVALID_TOKEN = 1 # GameId, Token pair does not match

