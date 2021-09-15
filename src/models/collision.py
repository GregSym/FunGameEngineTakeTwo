
from dataclasses import dataclass

from ..object import Object

@dataclass
class CollisionInfo:
    object: Object
    index: int
    angle: float

@dataclass
class CollisionEvent:
    has_vertical_collision: bool
    has_horizontal_collision: bool