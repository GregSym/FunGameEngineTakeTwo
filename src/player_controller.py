if __name__ == "__main__":
    from templates.controller_template import ControllerTemplate
    from context import Context
    from physics_model_generic import PhysicsModelGeneric
else:
    from .templates.controller_template import ControllerTemplate
    from .context import Context
    from src.physics_model_generic import PhysicsModelGeneric

from dataclasses import dataclass

from pygame import Vector2, event
import pygame
from typing import Callable

@dataclass
class KeyAction:
    key_down: Callable
    key_up: Callable


@dataclass
class KeyMap:
    """
        python dataclass for keymap, maybe should be a dict
    """
    left = pygame.K_a
    right = pygame.K_d
    jump = pygame.K_SPACE


class PlayerController(ControllerTemplate):
    """
        Controller for a player character
    """

    def __init__(self, context: Context, physics_model: PhysicsModelGeneric, key_map: KeyMap = KeyMap(),  max_velocity_x: int = 700) -> None:
        super().__init__()
        self.context = context
        self.physics_model = physics_model
        self.max_velocity_x = max_velocity_x
        self.acceleration_chunk = 200
        self.key_map = key_map
        self.move_left = KeyAction(key_down=lambda: self.__move_horizontal_keydown(
            direction='left'), key_up=lambda: self.__move_horizontal_keyup(direction='left'))
        """
            packages both keyup and keydown handlers
        """
        self.move_right = KeyAction(key_down=lambda: self.__move_horizontal_keydown(
            direction='right'), key_up=lambda: self.__move_horizontal_keyup(direction='right'))
        """
            packages both keyup and keydown handlers
        """

    def __reset_physics_x(self):
        self.physics_model.velocity.x = 0
        self.physics_model.acceleration.x = 0

    def __set_direction(self, direction: str):
        if direction == 'left':
            return -1 * self.acceleration_chunk
        else:
            return self.acceleration_chunk

    def __move_horizontal_keydown(self, direction: str):
        acceleration_chunk = self.__set_direction(direction=direction)
        if self.physics_model.velocity.x <= self.max_velocity_x:
            self.physics_model.acceleration.x += acceleration_chunk
        else:
            self.physics_model.acceleration.x = 0

    def __move_horizontal_keyup(self, direction: str):
        acceleration_chunk = self.__set_direction(direction=direction)
        self.__reset_physics_x()

    def get_events(self):
        for event in self.context.events:
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.key_map.left:
                self.move_left.key_down()
            if event.key == self.key_map.right:
                self.move_right.key_down()
        if event.type == pygame.KEYUP:
            if event.key == self.key_map.left:
                self.move_left.key_up()
            if event.key == self.key_map.right:
                self.move_right.key_up()
