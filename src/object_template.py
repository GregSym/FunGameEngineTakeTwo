from abc import ABC

class ObjectTemplate(ABC):
    """
        An abstract base class of the Objects instantiable within the Engine
    """
    def setup():
        """
            setup the object's initial state
        """
    
    def update():
        """
            Perform operations based on the latest scenario presented by the engine
        """

    def draw():

        """
            Draw the latest version of the object's state
        """