
from abc import ABC


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
