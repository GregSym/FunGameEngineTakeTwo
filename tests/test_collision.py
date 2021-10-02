import pygame
import random
from pygame.math import Vector2
import pytest
from pygame.rect import Rect
from GameThonic.EngineBits.functions.direction import CollisionSide, PhysxCalculations
from GameThonic.EngineBits.functions.random_item_generation import generate_random_rect

rect_side_list = [
    (Rect(0, 0, 4, 8), CollisionSide.TOP),
    (Rect(5, 4, 5, 4), CollisionSide.BOTTOM),
    (Rect(9, 3000, 1, 1), CollisionSide.LEFT),
    (Rect(450000, 23999, 32394, 31241324), CollisionSide.RIGHT)
]


def rect_side_pair_generator(rect: Rect) -> tuple[Rect, CollisionSide]:
    number = random.randint(1, 4)
    if number == 1:
        return (rect, CollisionSide.TOP)
    elif number == 2:
        return (rect, CollisionSide.BOTTOM)
    elif number == 3:
        return (rect, CollisionSide.LEFT)
    return (rect, CollisionSide.RIGHT)


def rect_side_list_generator(limit) -> list[tuple[Rect, CollisionSide]]:
    for i in range(limit):
        rect_side_list.append(rect_side_pair_generator(rect=generate_random_rect()))
    return rect_side_list


def test_collision_direction():
    """ Test that the current collision direction returns its own valid enums to mark direction """
    rect1 = pygame.Rect(4, 0, 5, 5)
    rect2 = pygame.Rect(4, 4, 6, 6)

    assert PhysxCalculations.relative_position(rect1=rect1, rect2=rect2) == CollisionSide.BOTTOM


@pytest.mark.parametrize(["rect", "side"], rect_side_list_generator(limit=100))
def test_collision_direction_general(rect: Rect, side: CollisionSide):
    """ More intensive testing, making some rect package assumptions """
    topleft = Vector2(rect.x, rect.y)
    width = random.randint(0, 1920)
    height = random.randint(0, 1080)  # any amount of pixels up to the avg. screen size

    def assertion() -> bool:
        test_rect = Rect(topleft.x, topleft.y, width, height)
        assert PhysxCalculations.collision_com(rect1=test_rect, rect2=rect) == side

    if side == CollisionSide.BOTTOM:
        topleft.y -= random.randint(1, height)
        assertion()
    elif side == CollisionSide.TOP:
        topleft.y += random.randint(int(rect.height * 3 / 4), rect.height)
        assertion()
    elif side == CollisionSide.RIGHT:
        topleft.x -= random.randint(0, width)
        assertion()
    elif side == CollisionSide.LEFT:
        topleft.x = random.randint(int(rect.right - width / 2), rect.right)
        assertion()
    else:
        print(" FAILURE IN TESTING PROTOCOL ")
        assert False
