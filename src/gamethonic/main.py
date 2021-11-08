# local imports
from gamethonic.enginebits import Camera
from gamethonic.enginebits import Layer
from gamethonic.enginebits import pyGameSetup
from gamethonic.enginebits import Player
from gamethonic.enginebits import PhysicsModelGeneric
from gamethonic.enginebits import Floor
from gamethonic.enginebits import Object
from gamethonic.enginebits import Context, SurfaceInfo
from gamethonic.enginebits import AppTemplate
from gamethonic.enginebits import EventLoopAsync
from gamethonic.enginebits import MetaGame

# Import non-standard modules.
import pygame
from pygame import event
from pygame import mouse, QUIT
from pygame import Vector2
import sys


class MainApp(AppTemplate):
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        dt, fps, clock, screen = pyGameSetup()
        self.context: Context = Context(
            fps=fps, dt=dt, clock=clock, screen=screen, surface_info=SurfaceInfo(
                width=640, height=480),
            events=event.get(), actions=[], scene={})

    def start(self):
        """ triggers the run method """
        self.run()

    def loop_logic(self):
        self.update()
        self.draw()
        # NOTE: .tick method returns milliseconds, hence /1000
        self.context.dt = self.context.clock.tick(self.context.fps) / 1000
        print(self.context.dt)

    def run(self):
        self.setup()
        print("fps is:", self.context.fps)
        while True:
            self.update()
            self.draw()
            # NOTE: .tick method returns milliseconds, hence /1000
            self.context.dt = self.context.clock.tick(self.context.fps) / 1000
            print(self.context.dt)


class MainAppAsync(EventLoopAsync):
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        dt, fps, clock, screen = pyGameSetup()
        self.context: Context = Context(
            fps=fps, dt=dt, clock=clock, screen=screen, surface_info=SurfaceInfo(
                width=640, height=480),
            events=event.get(), actions=[], scene={})

    def start(self):
        """ triggers the run method """
        self.run()

    async def loop_logic(self):
        await super().loop_logic()
        self.context.dt = self.context.clock.tick(self.context.fps) / 1000


class Engine(MainApp):
    """
        A game engine for handling full scenes of game objects
        and applying physics rules and event handlers upon such things
    """

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
        self.metagame: MetaGame = MetaGame()

    def update(self):
        """
        Update game. Called once per frame.
        """
        # Go through events that are passed to the script by the window.
        self.context.events = event.get()
        for _event in self.context.events:
            if _event.type == QUIT:
                pygame.quit()  # Opposite of pygame.init
                sys.exit()  # Not including this line crashes the script on Windows. Possibly
                # on other operating systems too, but I don't know for sure. - note from template
            if _event.type == pygame.MOUSEBUTTONUP:
                self.context.scene['player'].objects.append(Player(context=self.context, physics_model=PhysicsModelGeneric(
                    position=Vector2(mouse.get_pos()), velocity=Vector2(0, 0), has_gravity=True, acceleration=Vector2(0, 300), has_collision=True)))

        for index, action in enumerate(self.context.actions):
            """ Handles actions and deletes once executed """
            if action.update():
                self.context.actions.pop(index)

        for layer in self.context.scene.values():
            for object in layer.objects:
                object.update()

        self.metagame.update()

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
    engine = Engine()  # init and run engine - engine is currently run from the constructor/init method
    # those aren't the same thing but, like, whatevs
    engine.run()


if __name__ == "__main__":
    main()
