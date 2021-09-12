import dataclasses
if __name__=="__main__":
    from events.action import Action
else:
    from .events.action import Action
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
    events: list[event.Event]
    actions: list[Action]

    def add_action(self, action: Action):
        """ Adds an actions to the context.actions list to be executed as instructed as part of the event loop """
        self.actions.append(action)
