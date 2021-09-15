
if __name__ == "__main__":
    from context import Context, SurfaceInfo
    from templates.object_template import ObjectTemplate
    from physics_model_generic import PhysicsModelGeneric
    from functions.direction import PhysxCalculations
    import scene
else:
    try:
        from .context import Context, SurfaceInfo
        from .templates.object_template import ObjectTemplate
        from .physics_model_generic import PhysicsModelGeneric
        from .functions.direction import PhysxCalculations
        from . import scene
    except ImportError:
        from context import Context, SurfaceInfo
        from templates.object_template import ObjectTemplate
        from physics_model_generic import PhysicsModelGeneric
        from functions.direction import PhysxCalculations
        import scene


from src.models.collision import CollisionEvent
from pygame.constants import QUIT
from pygame.locals import Color
from typing import Any, Tuple
from pygame import Vector2, Surface, math, sprite
import pygame
import numpy as np


class Object(ObjectTemplate):
    """
        Object with methods for setup, update and draw
    """
    collision = CollisionEvent(has_vertical_collision=False, has_horizontal_collision=False)

    def __init__(self,
                 context: Context,
                 dimensions: Vector2 = Vector2(50, 50),
                 physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__()
        self.context = context
        self.dimensions = dimensions
        self.sprite = Surface(size=dimensions)
        self.sprite.fill(color=(255, 0, 0))
        self.rect = self.sprite.get_rect()
        self.physics_model = physics_model
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

    def __vertical_bounce(self):
        if self.physics_model.smooth_physics:
            if self.physics_model.acceleration.y >= self.physics_model.velocity.y:
                self.physics_model.velocity.y = 0
            else:
                self.physics_model.velocity.y = self.physics_model.velocity.y * \
                    (-.9)
        else:
            self.physics_model.velocity.y = self.physics_model.velocity.y * \
                (-.9)

    def handle_collision(self):
        collision_target = 'env'
        collision_layer = [self.context.scene.scene[key]
                           for key in self.context.scene.scene.keys() if key == collision_target][0]
        collision_objects = [
            object for object in collision_layer.objects if object.get_rect().colliderect(self)]

        for object in collision_objects:
            angle = PhysxCalculations.determineSide(self.rect, object.get_rect())
            if angle == np.pi / 2 or angle == 3 * np.pi / 2:
                self.collision.has_vertical_collision = True
            else:
                self.collision.has_horizontal_collision = True


    def update(self):
        self.physics_model.gravity_update(dt=self.context.dt)
        self.rect.x, self.rect.y = self.physics_model.position

    def draw(self):
        self.context.screen.blit(self.sprite, dest=self.rect)

    def reset(self, hard_reset: bool = False):
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(0, 0)

    def get_rect(self) -> pygame.Rect:
        return self.rect


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
    context = Context(fps=fps, dt=dt, clock=fpsClock,
                      screen=screen, surface_info=SurfaceInfo(width, height))

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
