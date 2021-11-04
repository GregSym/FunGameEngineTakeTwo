import dataclasses
from typing import Generator

from layout_manipulation import LayoutManipulation
if __name__ == "__main__":
    from events import Action
    from models.physics import WorldPhysics
    import scene
else:
    try:
        from .events import Action
        from .models.physics import WorldPhysics
        from . import scene
    except ImportError:
        try:
            from events import Action  # in the specific case where context is accessed relatively
            from models.physics import WorldPhysics
            import scene
        except ModuleNotFoundError:
            from gamethonic.enginebits.events import Action  # in the specific case where context is accessed relatively
            from gamethonic.enginebits.models.physics import WorldPhysics
            from gamethonic.enginebits import scene

from pygame.time import Clock
from pygame.surface import Surface
from pygame import Rect, event

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

    @property
    def grid(self) -> Generator[Rect, None, None]:
        """ A quick grid layout based on grid rules in world meta (TODO: make that) """
        _grid: Generator[Rect, None, None] = LayoutManipulation.grid_from_container(
            container_rect=self.screen.get_rect(), grid_width=10, grid_height=10)
        return _grid
