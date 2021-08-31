
from dataclasses import dataclass
from pygame import Vector2


@dataclass
class PhysicsModelGeneric:
    """
        Super-basic, generic physics model
        - pos @ origin, no velocity, no gravity
    """
    position: Vector2 = Vector2(0, 0)
    velocity: Vector2 = Vector2(0, 0)
    has_gravity: bool = False
