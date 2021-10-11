""" Storage for useful rect functions that aren't built into the class """
from pygame.math import Vector2
from pygame.rect import Rect


def rect_corners(rect: Rect) -> list[Vector2]:
    return [
        Vector2(rect.topleft), Vector2(rect.topright),
        Vector2(rect.bottomleft), Vector2(rect.bottomright)]


def rect_sides(rect: Rect) -> list[int]:
    return [
        rect.left, rect.right, rect.top, rect.bottom
    ]


def rect_all_points(rect: Rect) -> list[Vector2]:
    """ Returns all verteces in object starting topleft rotating clockwise to center left """
    return [Vector2(rect.topleft),
            Vector2(rect.centerx, rect.top),
            Vector2(rect.topright),
            Vector2(rect.right, rect.centery),
            Vector2(rect.bottomright),
            Vector2(rect.centerx, rect.bottom),
            Vector2(rect.bottomleft),
            Vector2(rect.left, rect.centery)]
