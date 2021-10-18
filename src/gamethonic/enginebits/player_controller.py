from gamethonic.enginebits.context import Context
from gamethonic.enginebits.physics_model_generic import PhysicsController, PhysicsModelGeneric

from dataclasses import dataclass
from gamethonic.enginebits.templates import HandlerTemplate
from gamethonic.enginebits.templates.key_press_action_template import ContinuousActionImplementation

from pygame import event
import pygame
from typing import Any, Callable


@dataclass
class KeyAction:
    key_down: Callable[..., Any]
    """ method to call while key is held """
    key_up: Callable[..., Any]
    """ method to call upon key release """


@dataclass
class KeyBinding:
    """
        python dataclass for keymap, maybe should be a dict
    """
    key: int
    key_action: KeyAction


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


class PlayerController(PhysicsController):
    def __init__(self, context: Context, physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__(context, physics_model=physics_model)
        self.handlers.insert(0, PlayerHandler(context=self.context, model=self.physics_model))


class PlayerHandler(HandlerTemplate):
    """
        Controller for a player character
    """

    def __init__(self, context: Context, model: PhysicsModelGeneric, max_velocity_x: float = 70) -> None:
        self.context = context
        self.model = model
        self.max_velocity_x = max_velocity_x
        self.acceleration_chunk: float = 200
        # default deceleration due to the virtual friction of the ground
        self.deceleration: float = self.acceleration_chunk * 2
        self.state = ControllerState()
        self.move_left = KeyBinding(key=pygame.K_a, key_action=KeyAction(key_down=lambda: self.__move_horizontal_keydown(
            direction='left'), key_up=lambda: self.__move_horizontal_keyup(direction='left')))
        """
            packages both keyup and keydown handlers
        """
        self.move_right = KeyBinding(key=pygame.K_d, key_action=KeyAction(key_down=lambda: self.__move_horizontal_keydown(
            direction='right'), key_up=lambda: self.__move_horizontal_keyup(direction='right')))
        """
            packages both keyup and keydown handlers
        """
        self.jump = KeyBinding(key=pygame.K_SPACE, key_action=KeyAction(
            key_down=lambda: self.__jump_keydown(), key_up=lambda: self.__jump_keyup()))
        self.control_scheme = [self.move_left, self.move_right, self.jump]

    def directionChanged(self) -> bool:
        """
            Has direction changed during the horizontal motion functional call
             - Returns True in between button press and acceleration past 0_.s-1
        """
        if self.acceleration_chunk * self.model.velocity.x < 0:
            return True
        else:
            return False

    def __reset_x(self):
        self.model.velocity.x = 0
        self.model.acceleration.x = 0
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
        if abs(self.model.velocity.x) <= self.max_velocity_x:
            self.model.acceleration.x = self.acceleration_chunk
        elif self.directionChanged():
            self.model.acceleration.x = self.acceleration_chunk
        else:
            self.model.acceleration.x = 0

    def __move_horizontal_keyup(self, direction: str):

        # def __private_test_decel():
        #     if self.model.velocity.x >= 0:
        #         self.model.velocity.x -= self.acceleration_chunk
        #     else:
        #         self.model.velocity.x = 0

        if self.acceleration_chunk * self.model.velocity.x >= 0:  # if acc. is still in the same direction
            # as vel. then reset the physics for now
            # self.context.actions.append(Action.do_until(
            #     action=lambda:  __private_test_decel(), duration=timedelta(seconds=2)))
            self.__reset_x()

    def __jump_keydown(self):
        def _jump():
            self.model.acceleration.y = -400

        def _slow_fall():
            self.model.acceleration.y = self.context.physics.gravity_constant / 2

        jump = ContinuousActionImplementation(context=self.context)
        jump.run_with_updates_declarative(init_action=_jump, during_action=_slow_fall)

    def __jump_keyup(self):
        self.model.acceleration.y = self.context.physics.gravity_constant

    def set_jump(self):
        self.state.is_grounded = True

    def input(self):
        self.get_events()

    def update(self):
        self.get_events()

    def get_events(self):
        for _event in self.context.events:
            self.handle_event(_event)

    def handle_event(self, event: event.Event):
        if event.type == pygame.KEYDOWN:
            for key_binding in self.control_scheme:
                if event.key == key_binding.key:
                    key_binding.key_action.key_down()
        if event.type == pygame.KEYUP:
            for key_binding in self.control_scheme:
                if event.key == key_binding.key:
                    key_binding.key_action.key_up()
