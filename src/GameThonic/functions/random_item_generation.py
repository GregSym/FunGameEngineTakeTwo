import random
from pygame.rect import Rect
from pygame.math import Vector2


def generate_random_rect() -> Rect:
    width = 1980
    height = 1080
    topleft = Vector2(
        x=random.randint(0, width),
        y=random.randint(0, height)
    )
    return Rect(topleft.x, topleft.y, random.randint(0, width), random.randint(0, height))
