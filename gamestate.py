import enum

class GameState(enum.Enum):
    Setup, Play, Win, Lose = range(4)