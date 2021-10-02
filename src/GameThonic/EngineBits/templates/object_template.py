from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2


class ObjectTemplate(ABC):
    """
        An abstract base class of the Objects instantiable within the Engine
    """

    @abstractmethod
    def setup(self):
        """
            setup the object's initial state
        """

    @abstractmethod
    def update(self):
        """
            Perform operations based on the latest scenario presented by the engine
        """

    @abstractmethod
    def draw(self):
        """
            Draw the latest version of the object's state
        """

    @abstractmethod
    def reset(self):
        """
            Reset the object parameters to default
        """

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        """
            Getter for the item's rect
        """

    @abstractmethod
    def get_surface(self) -> pygame.Surface:
        """
            Getter for the item's surface
        """

    def adjust_position(self, adjustment: Vector2):
        """ Adjust the object's position by the adjustment vector """

    def set_position(self, position: Vector2):
        """ Override the object's position with a new Vector2 """

    def get_velocity(self) -> Vector2:
        """ Getter for the object's velocity """

    def update_controller_collisions(self, angle: float):
        """
            communicate collision info to the controller, if there is one
        """

    def reset_controller_collisions(self):
        """
            reset controller state props, e.g. is_grounded
        """

    def collision_interacting_event(self):
        """
            insert functions that interact with the collision here
        """
