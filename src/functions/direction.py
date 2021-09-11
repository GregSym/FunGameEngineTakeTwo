import numpy as np
import pygame


class PhysxCalculations:
    """
        Generic helper functions for physics operations
    """

    @staticmethod
    def determineSide(rect1: pygame.Rect, rect2: pygame.Rect) -> float:
        """
            uses rects to determine the direction (rad) of collision of rect1 and rect2, relative to rect2
            - courtesy of adammoyle @ https://stackoverflow.com/questions/44119680/pygame-detect-collision-direction
            - currently only provides 4 possible directions
            - TODO: wrap in a class with more options than Rects that provide more directions
        """
        if rect1.midtop[1] > rect2.midtop[1]:
            return np.pi / 2
        elif rect1.midleft[0] > rect2.midleft[0]:
            return np.pi
        elif rect1.midright[0] < rect2.midright[0]:
            return 0
        else:
            return 3 * np.pi
