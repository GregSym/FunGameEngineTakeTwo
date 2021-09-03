
from dataclasses import dataclass

@dataclass
class Colours:
    red: tuple[int, int, int] = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)