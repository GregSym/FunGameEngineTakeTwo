
from dataclasses import dataclass
import enum


@dataclass
class CollisionEvent:
    has_vertical_collision: bool
    has_horizontal_collision: bool


class CollisionKeys(enum.Enum):
    """ Simplest possible tags for use in collision dicts by game objects and controllers """
    HORIZONTAL = enum.auto()
    VERTICAL = enum.auto()


class CollisionKeysDetailed(enum.Enum):
    """ 4 directional tags for use in collision dicts by game objects and controllers """
    TOP = enum.auto()
    BOTTOM = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class CollisionState(enum.Enum):
    MOMENTUM = enum.auto()
    """ Normal simplified Newtonian behaviour """
    SMOOTH = enum.auto()
    """ No vibrations or oscillations - object hits an item and stops """
