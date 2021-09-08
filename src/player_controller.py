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
from concurrent.futures import ThreadPoolExecutor
from typing import Callable


@dataclass
class KeyAction:
    key_down: Callable
    """ method to call while key is held """
    key_up: Callable
    """ method to call upon key release """


@dataclass
class KeyMap:
    """
        python dataclass for keymap, maybe should be a dict
    """
    left = pygame.K_a
    right = pygame.K_d
    jump = pygame.K_SPACE


@dataclass
class ControllerState:
    """
        Container for the state of a controller
    """
    is_moving: bool = False
    is_moving_left: bool = False
    is_moving_right: bool = False
    is_jumping: bool = False
    is_grounded: bool = False

    # important conditional
    left_down: bool = True
    right_down: bool = True
    left_down_right_up: bool = False
    right_down_left_up: bool = False


class PlayerController(ControllerTemplate):
    """
        Controller for a player character
    """

    def __init__(self, context: Context, physics_model: PhysicsModelGeneric, key_map: KeyMap = KeyMap(),  max_velocity_x: int = 70) -> None:
        super().__init__()
        self.context = context
        self.physics_model = physics_model
        self.max_velocity_x = max_velocity_x
        self.acceleration_chunk = 200
        # default deceleration due to the virtual friction of the ground
        self.deceleration = self.acceleration_chunk * 2
        self.key_map = key_map
        self.state = ControllerState()
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

    def directionChanged(self) -> bool:
        """
            Has direction changed during the horizontal motion functional call
             - Returns True in between button press and acceleration past 0_.s-1
        """
        if self.acceleration_chunk * self.physics_model.velocity.x < 0:
            return True
        else:
            return False

    def __reset_physics_x(self):
        self.physics_model.velocity.x = 0
        self.physics_model.acceleration.x = 0
        self.state.is_moving = False

    def __set_direction(self, direction: str):
        """ set the direction of the 1D acceleration """
        if direction == 'left':
            self.acceleration_chunk = -1 * abs(self.acceleration_chunk)
        else:
            self.acceleration_chunk = abs(self.acceleration_chunk)
        self.deceleration = self.deceleration * -1 * \
            abs(self.acceleration_chunk) / \
            self.acceleration_chunk  # set friction

    def __move_horizontal_keydown(self, direction: str):
        self.state.is_moving = True
        self.__set_direction(direction=direction)
        if self.directionChanged():
            print("Direction changed!")
        if abs(self.physics_model.velocity.x) <= self.max_velocity_x:
            self.physics_model.acceleration.x = self.acceleration_chunk
        elif self.directionChanged():
            self.physics_model.acceleration.x = self.acceleration_chunk
        else:
            self.physics_model.acceleration.x = 0

    def __move_horizontal_keyup(self, direction: str):
        if self.acceleration_chunk * self.physics_model.velocity.x >= 0:  # if acc. is still in the same direction
            # as vel. then reset the physics for now
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
