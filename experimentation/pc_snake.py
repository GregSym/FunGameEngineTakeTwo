from pygame.math import Vector2
from pygame.rect import Rect
from gamethonic.enginebits.context import Context
from gamethonic.enginebits import Object
from gamethonic.enginebits.templates import ControllerTemplate
from gamethonic.enginebits import PhysicsModelGeneric
import random


class SnakeSegment(Object):
    """ GameObject repr for segments of the snek """


class SnakeController(ControllerTemplate):
    def __init__(self) -> None:
        super().__init__()


class Snake:
    """ A repr of the player's snek """

    segments = []
    """ segments of the snek """

    def __init__(self, context: Context) -> None:
        self.context = context
        self.grid = list(self.context.grid)
        self.starting_position: Rect = self.grid[random.randint(0, len(self.grid))]
        self.segments.append(SnakeSegment(physics_model=PhysicsModelGeneric(position=Vector2(self.starting_position.topleft))))
        self.controller: ControllerTemplate = SnakeController()

    def elongate(self):
        self.segments.append(SnakeSegment())
