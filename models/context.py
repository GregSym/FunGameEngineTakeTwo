import dataclasses
from typing import Any

from pygame.time import Clock

@dataclasses.dataclass
class Context:
    fps: float
    dt: float
    clock: Clock
    screen: Any