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

    def update(self, events: list[event.Event]):
        super().update()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if abs(self.velocity.x) <= 500:
                        self.acceleration.x -= 500
                    else:
                        self.acceleration.x = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.reset()
