import dataclasses
if __name__ == "__main__":
    from events.action import Action
    from models.physics import WorldPhysics
    import scene
else:
    try:
        from .events.action import Action
        from .models.physics import WorldPhysics
        from . import scene
    except ImportError:
        from events.action import Action # in the specific case where context is accessed relatively
        from models.physics import WorldPhysics
        import scene


from typing import Any
import pygame

from pygame.time import Clock
from pygame import Surface, event

# NOTE: some of this may well run better with dicts, apparently, but I don't get
# linting from that so...no. Well, maybe later, actually


@dataclasses.dataclass
class SurfaceInfo:
    """
        A description of a surface, might be useful
    """
    width: int
    height: int


@dataclasses.dataclass
class Context:
    """
        dataclass for holding info regarding the overall world
    """
    fps: int  # stalls for other number types
    dt: float
    """ time-delta for framerate independent physics calculations """
    clock: Clock
    screen: Surface
    surface_info: SurfaceInfo
    scene: dict[str, scene.Layer]
    events: list[event.Event] = dataclasses.field(default_factory=lambda: [])
    actions: list[Action] = dataclasses.field(default_factory=lambda: [])
    physics: WorldPhysics = WorldPhysics()

    def add_action(self, action: Action):
        """ Adds an actions to the context.actions list to be executed as instructed as part of the event loop """
        self.actions.append(action)
