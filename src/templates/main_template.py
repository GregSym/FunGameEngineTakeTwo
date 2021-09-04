
import abc

class AppTemplate(abc.ABC):
    """
        The abstract base class defining the behaviour of a generic app based around
        pygame's use of drawing and SDL apis
    """
    def setup():
        """
            Setup the app's initial state and contents
        """

    def update():
        """
            Handle events
            Handle the change in screen img
        """

    def draw():
        """
        Draw things to the window. Called once per frame.
        """

    def run():
        """
            Runs the application
        """