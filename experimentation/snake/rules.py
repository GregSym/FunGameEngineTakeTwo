from abc import ABC, abstractmethod
import context
from gamethonic.enginebits import Context
import pc_snake
import food
from pygame.math import Vector2


class SnakeRule(ABC):

    def __init__(self, context: Context) -> None:
        self.context = context
        self.snake: pc_snake.Snake = pc_snake.Snake.of(context=self.context)
        self.food: food.Food = food.Food.of(context=self.context)

    @abstractmethod
    def rule_has_event(self) -> bool:
        """ does this rule have an event to act upon """

    @abstractmethod
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


class OurourobosRule(SnakeRule):
    """ Rule for when the snake hits itself """

    def rule_has_event(self) -> bool:
        for segment in self.snake.segments[1:]:
            if self.snake.segments[0] == segment:
                return True
        return False
    
    def on_rule_applicable(self):
        self.snake.reset()  # implement generic snake game reset

class BoundaryRule(SnakeRule):
    """ Rule for when snek hits the wall (this needs attachment to game state)
        states:
        - Kills the snake
        - Snek wraps around the board
    """

    def rule_has_event(self) -> bool:
        """ returns true when segments[0] is outside of grid """
        return self.snake.segments[0] not in self.context.grid

    def on_rule_applicable(self):
        self.snake.reset()  # implement generic snake game reset
