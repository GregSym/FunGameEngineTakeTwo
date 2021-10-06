# Import standard modules.
from EngineBits.camera import Camera
from EngineBits.templates.event_loop_item import EventLoopImplementation, EventLoopMultithreadedDraw
from EngineBits.scene import Layer, Scene
from EngineBits.events.action import Action
from EngineBits.settings.setup import pyGameSetup
from EngineBits.player import Player
from EngineBits.settings.settings import Settings
from EngineBits.physics_model_generic import PhysicsModelGeneric, PlayerPhysics
from EngineBits.floor import Floor
from EngineBits.object import Object
from EngineBits.context import Context, SurfaceInfo
from EngineBits.templates.main_template import AppTemplate

# Import non-standard modules.
import pygame
from pygame import event
from pygame.locals import *
from pygame import mouse, QUIT
from pygame import Vector2
from datetime import timedelta
from typing import Any
import sys


class MainApp(AppTemplate):
    def __init__(self) -> None:
        super().__init__()
        self.run()

    def setup(self):
        dt, fps, clock, screen = pyGameSetup()
        self.context: Context = Context(
            fps=fps, dt=dt, clock=clock, screen=screen, surface_info=SurfaceInfo(
                width=640, height=480),
            events=event.get(), actions=[], scene={})  

    def loop_logic(self):
        # NOTE: .tick method returns milliseconds, hence /1000
        self.context.dt = self.context.clock.tick(self.context.fps) / 1000
        print(self.context.dt)

    def run(self):
        self.setup()
        print(f"fps is:", self.context.fps)
        while True:
            self.update()
            self.draw()
            # NOTE: .tick method returns milliseconds, hence /1000
            self.context.dt = self.context.clock.tick(self.context.fps) / 1000
            print(self.context.dt)


class Engine(MainApp):

    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        super().setup()
        self.objects: list[Object] = [Object(context=self.context, physics_model=PhysicsModelGeneric(has_gravity=True))]
        self.context.scene['npc'] = Layer(objects=[Object(context=self.context, physics_model=PhysicsModelGeneric(has_gravity=True))])
        self.context.scene['player'] = Layer(objects=[])
        self.context.scene['env'] = Layer(objects=[Floor(
            context=self.context, physics_model=PhysicsModelGeneric(position=Vector2(0, 300)))])
        self.camera = Camera(context=self.context)

    def update(self):
        """
        Update game. Called once per frame.
        """
        # Go through events that are passed to the script by the window.
        self.context.events = pygame.event.get()
        for event in self.context.events:
            if event.type == QUIT:
                pygame.quit()  # Opposite of pygame.init
                sys.exit()  # Not including this line crashes the script on Windows. Possibly
                # on other operating systems too, but I don't know for sure. - note from template
            if event.type == pygame.MOUSEBUTTONUP:
                self.context.scene['player'].objects.append(Player(context=self.context, physics_model=PhysicsModelGeneric(
                    position=Vector2(mouse.get_pos()), velocity=Vector2(0, 0), has_gravity=True, acceleration=Vector2(0, 300), has_collision=True)))

        for index, action in enumerate(self.context.actions):
            """ Handles actions and deletes once executed """
            if action.update():
                self.context.actions.pop(index)

        for layer in self.context.scene.values():
            for object in layer.objects:
                object.update()

        self.camera.update()

    def draw(self):
        self.context.screen.fill((0, 255, 0))  # Fill the screen with black.

        # Redraw screen here.
        for layer in self.context.scene.values():
            for object in layer.objects:
                object.draw()
        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()


def main():
    """ Main functionality of the app """
    Engine()  # init and run engine - engine is currently run from the constructor/init method
    # those aren't the same thing but, like, whatevs


if __name__ == "__main__":
    main()
