from abc import ABC


class HandlerTemplate(ABC):
    """ A basic repr of how handlers will be interacted with by controllers """

    @staticmethod
    def update(self):
        """ A method to be called by the controller that owns this handler """