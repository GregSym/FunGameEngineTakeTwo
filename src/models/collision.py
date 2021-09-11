
from dataclasses import dataclass

from ..object import Object

@dataclass
class CollisionInfo:
    object: Object
    index: int
    angle: float

