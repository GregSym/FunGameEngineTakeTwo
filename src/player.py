"""
    Module pertaining to a rough mock-up of a player object
"""
if __name__ == "__main__":
    from object import Object
    from context import Context
    from physics_model_generic import PhysicsModelGeneric
    from constants.colours import Colours
else:
    from .object import Object
    from .context import Context
    from .physics_model_generic import PhysicsModelGeneric
    from .constants.colours import Colours

import numpy as np
from src.player_controller import PlayerController
from pygame import Vector2, event
import pygame


class Player(Object):
    def __init__(self,
                 context: Context,
                 dimensions: Vector2 = Vector2(50, 50),
                 physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__(context, dimensions=dimensions, physics_model=physics_model)
        self.sprite.fill(color=Colours.blue)
        self.max_velocity = 500
        self.controller = PlayerController(
            context=self.context, physics_model=self.physics_model)  # set a controller

    def update(self):
        super().update()
        self.controller.get_events()

    def update_controller_collisions(self, angle: float):
        if self.physics_model.acceleration.y >= self.physics_model.velocity.y:
            self.controller.state.is_grounded = True
        else:
            self.controller.state.is_grounded = False
