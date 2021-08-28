
from pygame.constants import QUIT
from pygame.locals import Color
from .context import Context
from typing import Tuple
from pygame import Vector2, Surface
import pygame
from .object_template import ObjectTemplate


class Object(ObjectTemplate):
    def __init__(self,
                 context: Context,
                 dimensions: Vector2 = Vector2(50, 50),
                 position: Vector2 = Vector2(0, 0),
                 has_gravity: bool = False) -> None:
        super().__init__()
        self.context = context
        self.dimensions = dimensions
        self.sprite = Surface(size=dimensions)
        self.sprite.fill(color=(255, 0, 0))
        self.position = position
        self.has_gravity = has_gravity

    def update(self):
        if self.has_gravity:
            self.position.y += 1

    def draw(self):
        self.context.screen.blit(self.sprite, dest=(
            self.position.x, self.position.y, self.dimensions.x, self.dimensions.y))


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
    context = Context(fps=fps, dt=dt, clock=fpsClock, screen=screen)

    test_object = Object(context=context)

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
