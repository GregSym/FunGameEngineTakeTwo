
if __name__ == "__main__":
    from context import Context, SurfaceInfo
    from templates.object_template import ObjectTemplate
    from physics_model_generic import PhysicsModelGeneric
else:
    try:
        from .context import Context, SurfaceInfo
        from .templates.object_template import ObjectTemplate
        from .physics_model_generic import PhysicsModelGeneric

    except ImportError:
        from context import Context, SurfaceInfo
        from templates.object_template import ObjectTemplate
        from physics_model_generic import PhysicsModelGeneric


from pygame.constants import QUIT
from pygame.locals import Color
from typing import Any, Tuple
from pygame import Vector2, Surface, sprite
import pygame
import numpy as np


class Object(ObjectTemplate):
    """
        Object with methods for setup, update and draw
    """

    def __init__(self,
                 context: Context,
                 dimensions: Vector2 = Vector2(50, 50),
                 physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__()
        self.context = context
        self.dimensions = dimensions
        self.physics_model = physics_model
        self.sprite = Surface(size=dimensions)
        self.sprite.fill(color=(255, 0, 0))
        self.rect = self.sprite.get_rect(topleft=(self.physics_model.position))
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

    def set_collision(self, collision: Any):
        if __name__ == "__main__":
            from scene import CollisionInfo
        else:
            try:
                from .scene import CollisionInfo
            except ImportError:
                from scene import CollisionInfo
        if collision.index != -1:
            self.collision: CollisionInfo = collision

    def __collision_info_import(self):
        if __name__ == "__main__":
            from scene import CollisionInfo
        else:
            try:
                from .scene import CollisionInfo
            except ImportError:
                from scene import CollisionInfo

    def handle_collision(self):
        if __name__ == "__main__":
            from scene import CollisionInfo
        else:
            try:
                from .scene import CollisionInfo
            except ImportError:
                from scene import CollisionInfo

        def __basic_vertical_collision(self: Object, collision: CollisionInfo):
            if collision.angle == np.pi / 2 or collision.angle == np.pi * 3 / 2:
                self.__vertical_bounce()
                self.collision = CollisionInfo(object=self, index=-1, angle=0)

        if hasattr(self, 'collision') and self.collision.index != -1:
            __basic_vertical_collision(self=self, collision=self.collision)

    def update(self):
        if hasattr(self, 'collision'):
            self.handle_collision()
        self.physics_model.gravity_update(dt=self.context.dt)
        self.draw()

    def draw(self):
        self.rect.x = self.physics_model.position.x
        self.rect.y = self.physics_model.position.y
        self.context.screen.blit(self.sprite, dest=(
            self.physics_model.position.x, self.physics_model.position.y, self.dimensions.x, self.dimensions.y))

    def reset(self, hard_reset: bool = False):
        self.physics_model.acceleration = Vector2(0, 0)
        self.physics_model.velocity = Vector2(0, 0)
        if hard_reset:
            self.physics_model.position = Vector2(0, 0)


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
