from abc import ABC
from gamethonic.enginebits import Context
import pc_snake
import food
from pygame.math import Vector2


class SnakeRule(ABC):

    def __init__(self, context: Context) -> None:
        self.context = context
        self.snake: pc_snake.Snake = pc_snake.Snake.of(context=self.context)
        self.food: food.Food = food.Food.of(context=self.context)

    def rule_has_event(self) -> bool:
        """ does this rule have an event to act upon """

    def on_rule_applicable(self):
        """ action to perform when rule_has_event returns True """

    def check_rule(self):
        """ entrypoint to be called in the event loop """
        if self.rule_has_event():
            self.on_rule_applicable()


class FoodRule(SnakeRule):
    """ The Snake rule for elongating the snek and incrementing the score """

    def rule_has_event(self) -> bool:
        return Vector2(self.snake.segments[0].get_rect().topleft) == self.food.model.position

    def on_rule_applicable(self):
        self.food.place()


class OurourobosRule:
    """ Rule for when the snake hits itself """


class BoundaryRule:
    """ Rule for when snek hits the wall (this needs attachment to game state)
        states:
        - Kills the snake
        - Snek wraps around the board
    """
