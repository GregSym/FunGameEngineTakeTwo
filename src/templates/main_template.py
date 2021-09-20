
import abc

class AppTemplate(abc.ABC):
    """
        The abstract base class defining the behaviour of a generic app based around
        pygame's use of drawing and SDL apis
    """

    @abc.abstractmethod
    def setup():
        """
            Setup the app's initial state and contents
        """

    @abc.abstractmethod
    def update():
        """
            Handle events
            Handle the change in screen img
        """

    @abc.abstractmethod
    def draw():
        """
        Draw things to the window. Called once per frame.
        """
        
    @abc.abstractmethod
    def run():
        """
            Runs the application
        """