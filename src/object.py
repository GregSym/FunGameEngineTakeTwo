
if __name__ == "__main__":
    from templates.object_template import ObjectTemplate
    from physics_model_generic import PhysicsModelGeneric
    from functions.direction import PhysxCalculations
    import context
    from models.collision import CollisionEvent
    import scene
else:
    try:
        from .templates.object_template import ObjectTemplate
        from .physics_model_generic import PhysicsModelGeneric
        from .functions.direction import PhysxCalculations
        from .models.collision import CollisionEvent
        from . import context
        from . import scene
    except ImportError:
        from templates.object_template import ObjectTemplate
        from physics_model_generic import PhysicsModelGeneric
        from functions.direction import PhysxCalculations
        from models.collision import CollisionEvent
        import context
        import scene


from dataclasses import dataclass
from src.models.collision import CollisionKeys
from pygame.constants import QUIT
from pygame.locals import Color
from typing import Any, Tuple
from pygame import Vector2, Surface, math, sprite
import pygame
import numpy as np
from enum import Enum, auto


class Object(ObjectTemplate):
    """
        Object with methods for setup, update and draw
    """
    collision = CollisionEvent(
        has_vertical_collision=False, has_horizontal_collision=False)
    collision_objects: dict[CollisionKeys, ObjectTemplate] = {}
    collision_target = 'env'

    def __init__(self,
                 context: context.Context,
                 dimensions: Vector2 = Vector2(50, 50),
                 physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__()
        self.context = context
        self.dimensions = dimensions
        self.sprite = Surface(size=dimensions)
        self.sprite.fill(color=(255, 0, 0))
        self.rect = self.sprite.get_rect()
        self.physics_model = physics_model
        self.setup()

    def setup(self):
        if self.physics_model.has_gravity:
            self.physics_model.acceleration = Vector2(0, 300)
        else:
            self.physics_model.acceleration = Vector2(0, 0)

    def test_collision(self, obj):
        """
            manual collision detector, to be privated
        """
        if self.physics_model.position.y + self.dimensions.y >= obj.physics_model.position.y:
            # self.acceleration = Vector2(0, 0)
            self.__vertical_bounce()

    def handle_collision(self):
        if CollisionKeys.VERTICAL in self.collision_objects:
            self.physics_model.handle_vertical_collision()
            self.collision.has_vertical_collision = False
            self.collision_objects.pop(CollisionKeys.VERTICAL)
        elif CollisionKeys.HORIZONTAL in self.collision_objects:
            self.physics_model.handle_horizontal_collision()
            self.collision.has_vertical_collision = True
            self.collision_objects.pop(CollisionKeys.HORIZONTAL)

    def get_collision(self):
        if self.collision_target in self.context.scene:
            collision_layer = self.context.scene[self.collision_target]
            collision_objects = [
                object for object in collision_layer.objects if self.rect.colliderect(
                    object.get_rect().x, object.get_rect().y - 3, object.get_rect().right, object.get_rect().bottom)]
            for object in collision_objects:
                angle = PhysxCalculations.determineSide(
                    self.rect, object.get_rect())
                self.angle = angle
                if angle == np.pi / 2 or angle == 3 * np.pi / 2:
                    self.update_controller_collisions(angle=angle)
                    if CollisionKeys.VERTICAL not in self.collision_objects:
                        self.collision.has_vertical_collision = True
                        self.collision_objects[CollisionKeys.VERTICAL] = object
                else:
                    if CollisionKeys.HORIZONTAL not in self.collision_objects:
                        self.collision.has_horizontal_collision = True
                        self.collision_objects[CollisionKeys.HORIZONTAL] = object
                if self.collision.has_horizontal_collision and self.collision.has_vertical_collision:
                    # reduces unecessary looping
                    return
        return

    def update(self):
        self.get_collision()
        self.handle_collision() 
        self.collision_interacting_event()
        self.physics_model.gravity_update(dt=self.context.dt)
        self.rect.x, self.rect.y = self.physics_model.position

    def draw(self):
        self.context.screen.blit(self.sprite, dest=self.rect)

    def reset(self, hard_reset: bool = False):
        self.physics_model.acceleration = Vector2(0, 0)
        self.physics_model.velocity = Vector2(0, 0)
        if hard_reset:
            self.physics_model.position = Vector2(0, 0)

    def adjust_position(self, adjustment: Vector2):
        self.physics_model.position += adjustment * self.context.dt

    def set_position(self, position: Vector2):
        self.physics_model.position = position

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_surface(self) -> pygame.Surface:
        return self.sprite


if __name__ == "__main__":
    import sys
    """local test"""
    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 144
    fpsClock = pygame.time.Clock()

    # Set up the window.
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt = 1/fps  # dt is the time since last frame.
    context = context.Context(fps=fps, dt=dt, clock=fpsClock,
                              screen=screen, surface_info=context.SurfaceInfo(width, height))

    test_object = Object(context=context, physics_model=PhysicsModelGeneric())

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        """
        Draw things to the window. Called once per frame.
        """
        screen.fill((0, 255, 0))  # Fill the screen with black.

        # Redraw screen here.
        test_object.draw()
        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
