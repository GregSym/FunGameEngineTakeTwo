import dataclasses
from typing import Any

from pygame.time import Clock
from pygame import Surface

@dataclasses.dataclass
class Context:
    fps: int # stalls for other number types
    dt: float
    clock: Clock
    screen: Surface