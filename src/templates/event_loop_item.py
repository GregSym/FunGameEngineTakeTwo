
from abc import ABC
from concurrent.futures import ProcessPoolExecutor


class EventLoopItem(ABC):
    """
        A general structure for items in an event loop
    """

    def setup():
        """
            run before the start of the loop
             - sets up some initial state
             - can be called as part of __init__()
        """

    def loop_logic():
        """
            update and draw are called iteratively inside this function
        """

    def update():
        """
            The main method to be called iteratively as part of the 
            event loop
        """

    def draw():
        """
            A particular section of the update seperated out from update
            because the graphics API shouldn't be too deeply entangled with
            regular business logic
        """
class EventLoopImplementation(EventLoopItem):
    """
        An implementation of a basic event-loop
        - triggered by using the run() -> None method
    """

    def loop_logic(self):
        self.update()
        self.draw()

    def run(self):
        """ runs the event loop """
        self.setup()
        while True:
            self.loop_logic()

class EventLoopMultithreadedDraw(EventLoopImplementation):
    def loop_logic(self):
        with ProcessPoolExecutor() as executor:
            p1 = executor.submit(lambda: self.update())
            p2 = executor.submit(lambda: self.draw())