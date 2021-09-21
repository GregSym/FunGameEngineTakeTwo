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
        if rect1.top > rect2.top or rect1.bottom < rect2.top:
            return np.pi / 2
        elif rect1.midleft[0] > rect2.midleft[0]:
            return np.pi
        elif rect1.midright[0] < rect2.midright[0]:
            return 0
        else:
            return 3 * np.pi

    @staticmethod
    def collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        if (rect2.bottom <= rect1.bottom < rect2.top) or (rect1.bottom <= rect2.bottom < rect1.top) or ((rect1.top <= rect2.top) and (rect2.top > rect1.bottom)) or ((rect2.top <= rect1.top) and (rect1.top > rect2.bottom)) or ((rect1.top < rect2.top) and (rect2.bottom <= rect1.top)) or ((rect1.bottom <= rect2.top) and (rect1.bottom > rect2.bottom)):
            if (rect2.left <= rect1.right < rect2.right) or (rect1.left <= rect2.right < rect1.right):
                return True
        return False

