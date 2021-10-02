from abc import ABC

class ControllerTemplate(ABC):

    def key_response():
        """
            Response to a keypress
        """

    def get_events():
        """
            Get a list of available events
        """

    def handle_event():
        """
            match methods to appropriate events
        """