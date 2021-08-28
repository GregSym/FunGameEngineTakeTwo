# Import standard modules.
from models.object import Object
from models.context import Context
from typing import Any
from main_template import AppTemplate
import sys
 
# Import non-standard modules.
import pygame
from pygame.locals import *

def pyGameSetup() -> tuple[int, float, pygame.time.Clock, pygame.Surface]:
    # Initialise PyGame.
  pygame.init()
  
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
  dt: float = 1/fps # dt is the time since last frame.
  return dt, fps, fpsClock, screen

class MainApp(AppTemplate):
    def __init__(self) -> None:
        super().__init__()
        fps, dt, clock, screen = pyGameSetup()
        self.context: Context = Context(fps=fps, dt=dt, clock=clock, screen=screen)
        self.run()

    def run(self):
        self.setup()
        while True:
            self.update()
            self.draw()
            self.context.clock.tick(self.context.fps.__int__())


class Engine(MainApp):

    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        self.objects = [Object(context=self.context, has_gravity=True)]

    def update(self):
        """
        Update game. Called once per frame.
        dt is the amount of time passed since last frame.
        If you want to have constant apparent movement no matter your framerate,
        what you can do is something like
        
        x += v * dt
        
        and this will scale your velocity based on time. Extend as necessary.
        """
        # Go through events that are passed to the script by the window.
        for event in pygame.event.get():
            # We need to handle these events. Initially the only one you'll want to care
            # about is the QUIT event, because if you don't handle it, your game will crash
            # whenever someone tries to exit.
            if event.type == QUIT:
                pygame.quit() # Opposite of pygame.init
                sys.exit() # Not including this line crashes the script on Windows. Possibly
                # on other operating systems too, but I don't know for sure.
                # Handle other events as you wish.

        for object in self.objects:
            object.update()

    def draw(self):
        self.context.screen.fill((0, 255, 0)) # Fill the screen with black.
        
        # Redraw screen here.
        for object in self.objects:
            object.context = self.context
            object.draw()
        
        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()

if __name__=="__main__":
    Engine()