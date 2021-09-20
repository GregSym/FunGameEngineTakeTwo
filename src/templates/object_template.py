from abc import ABC, abstractmethod

import pygame


class ObjectTemplate(ABC):
    """
        An abstract base class of the Objects instantiable within the Engine
    """

    @abstractmethod
    def setup():
        """
            setup the object's initial state
        """

    @abstractmethod
    def update():
        """
            Perform operations based on the latest scenario presented by the engine
        """

    @abstractmethod
    def draw():
        """
            Draw the latest version of the object's state
        """

    @abstractmethod
    def reset():
        """
            Reset the object parameters to default
        """

    @abstractmethod
    def get_rect() -> pygame.Rect:
        """
            Getter for the item's rect
        """

    @abstractmethod
    def get_surface() -> pygame.Surface:
        """
            Getter for the item's surface
        """

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
