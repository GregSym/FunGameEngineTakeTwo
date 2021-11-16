from typing import Protocol
from pygame.math import Vector2
from pygame.rect import Rect
from gamethonic.enginebits import Context
from gamethonic.enginebits import Object
from gamethonic.enginebits import PhysicsModelGeneric
import random

from gamethonic.enginebits.templates import ObjectTemplate


class SegmentedGameObject(Protocol):
    segments: list[ObjectTemplate]


class Food(Object):
    """ GameObject repr of food """

    def __init__(self, context: Context, physics_model: PhysicsModelGeneric) -> None:
        super().__init__(context, physics_model=physics_model)

    def _valid_squares(self, snake: SegmentedGameObject) -> list[Rect]:
        """ private: return valid squares """
        return [
            position for position in self.context.grid if position.topleft not in [
                segment.get_rect().topleft for segment in snake.segments]]

    def place(self):
        """ randomly place the piece of food on a valid square """
        random_placement = random.randint(0, len(valid_squares := self._valid_squares(snake=self.context.scene['snake'].objects[0])))
        self.set_position(position=Vector2(valid_squares[random_placement].topleft))
