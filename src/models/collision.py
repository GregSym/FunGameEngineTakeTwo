
from dataclasses import dataclass


@dataclass
class CollisionEvent:
    has_vertical_collision: bool
    has_horizontal_collision: bool
