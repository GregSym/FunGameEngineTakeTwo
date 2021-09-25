from dataclasses import asdict, dataclass
from enum import Enum, auto
import numpy as np
import pygame
from pygame.math import Vector2
from pygame.rect import Rect


def rect_corners(rect: pygame.Rect) -> list[pygame.Vector2]:
    return [
        Vector2(rect.topleft), Vector2(rect.topright),
        Vector2(rect.bottomleft), Vector2(rect.bottomright)]


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
        return np.arccos(np.clip(np.dot(unit_vector1, unit_vector2), -1, 1))

    @staticmethod
    def boundary_calculation(angles: FourAngles):
        print([angle / np.pi for angle in asdict(angles).values()])
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
    def relative_position(rect1: pygame.Rect, rect2: pygame.Rect) -> CollisionSide:
        x_axis = Vector2(1, 0)
        ref_vector = Vector2(rect1.x, rect1.y)
        triangulation_vectors: list[Vector2] = []
        for corner_vector in rect_corners(rect=rect2):
            triangulation_vectors.append(corner_vector - ref_vector)
        angle_vector = Vector2(rect2.x - rect1.x, rect2.y - rect1.y)
        angles = FourAngles.from_list(vectors=triangulation_vectors)
        return PhysxCalculations.boundary_calculation(angles=angles)

    @staticmethod
    def collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        if (rect2.bottom <= rect1.bottom < rect2.top) or (rect1.bottom <= rect2.bottom < rect1.top) or ((rect1.top <= rect2.top) and (rect2.top > rect1.bottom)) or ((rect2.top <= rect1.top) and (rect1.top > rect2.bottom)) or ((rect1.top < rect2.top) and (rect2.bottom <= rect1.top)) or ((rect1.bottom <= rect2.top) and (rect1.bottom > rect2.bottom)):
            if (rect2.left <= rect1.right < rect2.right) or (rect1.left <= rect2.right < rect1.right):
                return True
        return False


if __name__ == "__main__":
    print(np.arctan([np.tan(angle.value)
          for angle in BoundaryConditions]) / np.pi)
    x_axis = Vector2(1, 0)
    test = Vector2(3, -3)
    print(PhysxCalculations.angle_calculation(vector1=x_axis, vector2=test))
    print(test.angle_to(x_axis) * -np.pi / 180 if test.angle_to(x_axis) * -np.pi / 180 >= 0 else test.angle_to(x_axis) * -np.pi / 180 + 2*np.pi)

    rect1 = pygame.Rect(9, 8, 5, 5)
    rect2 = Rect(4, 4, 6, 6)
    print(PhysxCalculations.relative_position(rect1=rect1, rect2=rect2))
