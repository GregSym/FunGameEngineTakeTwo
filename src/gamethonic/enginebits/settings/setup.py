if __name__ == "__main__":
    from settings import Settings
else:
    from .settings import Settings
import pygame
from pygame import surface, display


def pyGameSetup() -> tuple[float, int, pygame.time.Clock, surface.Surface]:
    """
        Generic method for pygame init
    """
    # Initialise PyGame.
    pygame.init()
    # key.set_repeat(1, 500) # this will probably be necessary at some point

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = Settings.fps
    fpsClock = pygame.time.Clock()

    # Set up the window.
    width, height = Settings.resolution
    try:
        screen = display.set_mode((width, height))
    except pygame.error:
        import os
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        screen = display.set_mode((width, height))


    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt: float = Settings.dt  # dt is the time since last frame.
    return dt, fps, fpsClock, screen
