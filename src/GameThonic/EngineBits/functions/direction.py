from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
import numpy as np
import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from .rect_wrapper import rect_all_points, rect_corners


class BoundaryConditions(Enum):
    ZERO: float = 0
    FORTYFIVE: float = np.pi / 4
    NINETY: float = np.pi / 2
    FLAT: float = np.pi
    BOTTOM: float = - np.pi / 2


@dataclass
class FourAngles:
    top_left: float
    top_right: float
    bottom_left: float
    bottom_right: float

    @classmethod
    def from_list(self, vectors: list[Vector2]):
        x_axis = Vector2(1, 0)
        angles = [vector.angle_to(x_axis) * -np.pi / 180 if vector.angle_to(x_axis) * -np.pi /
                  180 >= 0 else vector.angle_to(x_axis) * -np.pi / 180 + 2*np.pi for vector in vectors]
        return self(
            top_left=angles[0],
            top_right=angles[1],
            bottom_left=angles[2],
            bottom_right=angles[3]
        )


class CollisionSide(Enum):
    RIGHT = auto()
    LEFT = auto()
    TOP = auto()
    BOTTOM = auto()
    UNDEFINED = auto()  # maybe don't want this one


class _CollisionFunctionType(Protocol):
    def __call__(self, rect1: Rect, rect2: Rect) -> CollisionSide:
        """ A function type that takes in two rects and returns a collision direction """


def index_to_side(index: int) -> CollisionSide:
    if index == 0:
        return CollisionSide.BOTTOM
    if index == 1:
        return CollisionSide.TOP
    if index == 2:
        return CollisionSide.RIGHT
    if index == 3:
        return CollisionSide.LEFT
    return CollisionSide.UNDEFINED


class PhysxCalculations:
    """
        Generic helper functions for physics operations
    """

    @staticmethod
    def determineSide(rect1: Rect, rect2: Rect) -> float:
        """
            uses rects to determine the direction (rad) of collision of rect1 and rect2, relative to rect2
            - courtesy of adammoyle @ https://stackoverflow.com/questions/44119680/pygame-detect-collision-direction
            - currently only provides 4 possible directions
            - TODO: wrap in a class with more options than Rects that provide more directions
        """
        if rect1.top > rect2.top or rect1.bottom <= rect2.top:
            return np.pi / 2
        elif rect1.midleft[0] > rect2.midleft[0]:
            return np.pi
        elif rect1.midright[0] < rect2.midright[0]:
            return 0
        else:
            return 3 * np.pi

    @staticmethod
    def angle_calculation(vector1: Vector2, vector2: Vector2) -> float:
        unit_vector1 = vector1.normalize()  # vector / |vector|
        unit_vector2 = vector2.normalize()
        # similar performance to pygame version
        angle: float = np.arccos(np.clip(np.dot(unit_vector1, unit_vector2), -1, 1))  # unclear return type here apparently
        return angle

    @staticmethod
    def boundary_calculation(angles: FourAngles) -> CollisionSide:
        if angles.top_left < BoundaryConditions.FORTYFIVE.value and angles.bottom_left > 0:
            return CollisionSide.RIGHT
        if angles.top_left >= BoundaryConditions.FORTYFIVE.value and angles.top_right < BoundaryConditions.NINETY.value:
            return CollisionSide.BOTTOM
        if angles.bottom_left >= BoundaryConditions.FLAT.value and angles.bottom_right <= BoundaryConditions.NINETY.value:
            return CollisionSide.TOP
        if abs(angles.top_right) <= BoundaryConditions.NINETY.value and angles.bottom_right >= BoundaryConditions.NINETY.value:
            return CollisionSide.LEFT
        else:
            return CollisionSide.UNDEFINED

    @staticmethod
    def relative_position(rect1: Rect, rect2: Rect) -> CollisionSide:
        """ determine relative position using triangulation between rect corners """
        # x_axis = Vector2(1, 0)
        ref_vector = Vector2(rect1.x, rect1.y)
        triangulation_vectors: list[Vector2] = []
        for corner_vector in rect_corners(rect=rect2):
            triangulation_vectors.append(corner_vector - ref_vector)
        # angle_vector = Vector2(rect2.x - rect1.x, rect2.y - rect1.y)
        angles = FourAngles.from_list(vectors=triangulation_vectors)
        return PhysxCalculations.boundary_calculation(angles=angles)

    @staticmethod
    def collision(rect1: Rect, rect2: Rect) -> bool:
        if (rect2.bottom <= rect1.bottom < rect2.top) or (rect1.bottom <= rect2.bottom < rect1.top) or (
            (rect1.top <= rect2.top) and (rect2.top > rect1.bottom)) or (
                (rect2.top <= rect1.top) and (rect1.top > rect2.bottom)) or (
                    (rect1.top < rect2.top) and (rect2.bottom <= rect1.top)) or (
                        (rect1.bottom <= rect2.top) and (rect1.bottom > rect2.bottom)):
            if (rect2.left <= rect1.right < rect2.right) or (rect1.left <= rect2.right < rect1.right):
                return True
        return False

    @staticmethod
    def collision_com(rect1: Rect, rect2: Rect) -> CollisionSide:
        """ Determine relative position using relative position of the center of mass of rect1
            - relative position to rect1, eg. rect1 left of rect2 -> CollisionSide.RIGHT
        """
        if rect2.left <= rect1.centerx <= rect2.right:  # vertical collision
            if rect1.centery <= rect2.top:
                return CollisionSide.BOTTOM
            if rect1.centery >= rect2.bottom:
                return CollisionSide.TOP

        #  alt case where rect2 is smaller
        if rect1.left <= rect2.centerx <= rect1.right:
            if rect2.centery <= rect1.top:
                return CollisionSide.TOP
            if rect2.centery >= rect1.bottom:
                return CollisionSide.BOTTOM

        alt_result = PhysxCalculations.collision_full_frame_alt(rect1, rect2)
        # if alt_result != CollisionSide.TOP:
        #     return alt_result

        if rect1.centerx <= rect2.left:
            return CollisionSide.RIGHT
        if rect1.centerx >= rect2.right:
            if rect1.centery <= rect2.top:
                return CollisionSide.BOTTOM
            if rect1.centery >= rect2.bottom:
                return CollisionSide.TOP if alt_result == CollisionSide.TOP else CollisionSide.LEFT
            return CollisionSide.LEFT

        if rect2.centerx <= rect1.left:
            return CollisionSide.LEFT
        if rect2.centerx >= rect1.right:
            return CollisionSide.RIGHT

        def local_converter(relative_sides: list[int]) -> CollisionSide:
            for index, side in enumerate(relative_sides):
                if side == min(relative_sides):
                    return index_to_side(index=index)
            return CollisionSide.UNDEFINED

        # alt backup determination
        side_distances = [relative_vector for relative_vector in [rect2.top - rect2.centery,
                                                                  rect2.bottom - rect1.centery,
                                                                  rect2.left - rect1.centerx,
                                                                  rect2.right - rect1.centerx]]
        return local_converter(relative_sides=side_distances)

    @staticmethod
    def collision_combination(rect1: Rect, rect2: Rect) -> CollisionSide:
        triangulation = PhysxCalculations.relative_position(rect1, rect2)
        centre_of_mass = PhysxCalculations.collision_com(rect1, rect2)
        return triangulation if triangulation != CollisionSide.UNDEFINED else centre_of_mass

    @staticmethod
    def collision_full_frame(rect1: Rect, rect2: Rect) -> CollisionSide:
        """ relativity using all available points """
        # store_all_points_rect1 = rect_all_points(rect1)
        store_all_points = rect_all_points(rect2)  # only run this once
        right_positioned = [point for point in store_all_points if point.x >= rect1.centerx]
        bottom_positioned = [point for point in store_all_points if point.y >= rect1.centery]
        if len(bottom_positioned) > len(store_all_points) - len(bottom_positioned):
            return CollisionSide.BOTTOM
        if len(right_positioned) >= len(store_all_points) - len(right_positioned):
            return CollisionSide.LEFT

        mass_totals = [
            len(bottom_positioned),
            len(store_all_points) - len(bottom_positioned),
            len(store_all_points) - len(right_positioned),
            len(right_positioned)]
        for index, mass_total in enumerate(mass_totals):
            if mass_total == max(mass_totals):
                return index_to_side(index)

        return CollisionSide.UNDEFINED

    @staticmethod
    def collision_full_frame_alt(rect1: Rect, rect2: Rect) -> CollisionSide:
        """ relativity using all available points *alt """
        store_all_points = rect_all_points(rect1)  # only run this once
        points_above_rect2 = [point for point in store_all_points if point.y <= rect2.top]
        points_below_rect2 = [point for point in store_all_points if point.y >= rect2.bottom]
        points_left_rect2 = [point for point in store_all_points if point.x <= rect2.left]
        points_right_rect2 = [point for point in store_all_points if point.x >= rect2.right]

        mass_totals = [len(points_above_rect2),
                       len(points_below_rect2),
                       len(points_left_rect2),
                       len(points_right_rect2)]
        for index, mass_total in enumerate(mass_totals):
            if mass_total == max(mass_totals):
                return index_to_side(index)

        return CollisionSide.UNDEFINED

    @staticmethod
    def get_collision(rect: Rect,
                      target_rects: list[Rect],
                      collision_function: _CollisionFunctionType) -> dict[CollisionSide, CollisionSide]:
        """ Creates a full 2D collision event for a given rect and target group of rects """
        collision_event: dict[CollisionSide, CollisionSide] = {}
        collision_side: list[CollisionSide] = [
            collision_function(rect1=rect, rect2=_rect) for _rect in target_rects if rect.colliderect(_rect)]
        for side in collision_side:
            if side not in collision_event:
                collision_event[side] = side
            if len([collision_event.keys()]) == 4:
                return collision_event
        return collision_event


if __name__ == "__main__":
    print(np.arctan([np.tan(angle.value)
          for angle in BoundaryConditions]) / np.pi)
    x_axis = Vector2(1, 0)
    test = Vector2(3, -3)
    print(PhysxCalculations.angle_calculation(vector1=x_axis, vector2=test))
    print(test.angle_to(x_axis) * -np.pi / 180 if test.angle_to(x_axis) * -np.pi / 180 >= 0 else test.angle_to(x_axis) * -np.pi / 180 + 2*np.pi)

    rect1 = pygame.Rect(9, 8, 5, 5)
    rect2 = pygame.Rect(4, 4, 6, 6)
    print(PhysxCalculations.relative_position(rect1=rect1, rect2=rect2))
