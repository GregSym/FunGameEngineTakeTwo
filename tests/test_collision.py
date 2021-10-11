import pygame
import random
from pygame.math import Vector2
import pytest
from pygame.rect import Rect
import functions
from gamethonic.enginebits.functions import direction
from gamethonic.enginebits.functions import random_item_generation

rect_side_list = [
    (Rect(0, 0, 4, 8), direction.CollisionSide.TOP),
    (Rect(5, 4, 5, 4), direction.CollisionSide.BOTTOM),
    (Rect(9, 3000, 1, 1), direction.CollisionSide.LEFT),
    (Rect(450000, 23999, 32394, 31241324), direction.CollisionSide.RIGHT)
]


def rect_side_pair_generator(rect: Rect) -> tuple[Rect, direction.CollisionSide]:
    number = random.randint(1, 4)
    if number == 1:
        return (rect, direction.CollisionSide.TOP)
    elif number == 2:
        return (rect, direction.CollisionSide.BOTTOM)
    elif number == 3:
        return (rect, direction.CollisionSide.LEFT)
    return (rect, direction.CollisionSide.RIGHT)


def rect_side_list_generator(limit) -> list[tuple[Rect, direction.CollisionSide]]:
    for i in range(limit):
        rect_side_list.append(rect_side_pair_generator(rect=random_item_generation.generate_random_rect()))
    return rect_side_list


def test_collision_direction():
    """ Test that the current collision direction returns its own valid enums to mark direction """
    rect1 = pygame.Rect(4, 0, 5, 5)
    rect2 = pygame.Rect(4, 4, 6, 6)

    assert direction.PhysxCalculations.relative_position(rect1=rect1, rect2=rect2) == direction.CollisionSide.BOTTOM


@pytest.mark.parametrize(["rect", "side"], rect_side_list_generator(limit=100))
def test_collision_direction_general(rect: Rect, side: direction.CollisionSide):
    """ More intensive testing, making some rect package assumptions
        - still quite a general test - allows horizontal / vertical collision confusion edge cases
    """
    topleft = Vector2(rect.x, rect.y)
    width = random.randint(0, 1920)
    height = random.randint(0, 1080)  # any amount of pixels up to the avg. screen size

    def assertion() -> bool:
        test_rect = Rect(topleft.x, topleft.y, width, height)
        detected = direction.PhysxCalculations.collision_com(rect1=test_rect, rect2=rect)
        assert detected == side if not (
            side == direction.CollisionSide.LEFT
            or side == direction.CollisionSide.RIGHT
            and detected == direction.CollisionSide.TOP
            or detected == direction.CollisionSide.BOTTOM
        ) else True

    if side == direction.CollisionSide.BOTTOM:
        topleft.y -= random.randint(int(height / 2 if height <= rect.height else height - 1), height)
        assertion()
    elif side == direction.CollisionSide.TOP:
        topleft.y = random.randint(int(rect.bottom - min(height / 2, rect.height / 2)), rect.bottom)
        assertion()
    elif side == direction.CollisionSide.RIGHT:
        topleft.x -= random.randint(int(width / 2), width)
        assertion()
    elif side == direction.CollisionSide.LEFT:
        topleft.x = random.randint(int(rect.right - min(width / 2, rect.width / 2)), rect.right)
        assertion()
    else:
        print(" FAILURE IN TESTING PROTOCOL ")
        assert False
