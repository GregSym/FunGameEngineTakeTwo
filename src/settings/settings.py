"""
    File for storing relevant settings in a dataclass
    - might expose in an .config at some point?
"""
from dataclasses import dataclass

@dataclass
class Settings:
    fps = 144
    """ The maximum number of frames-per-second """
    dt = 1 / fps
    """ Time-delta between loops """
    width, height = 640, 480
    """ Dimensions of the screen in the x or y direction """
    resolution = width, height
    """ Resolution of the screen -> tuple[width: int, height: int] """