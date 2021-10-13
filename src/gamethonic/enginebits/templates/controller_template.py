from abc import ABC


class ControllerTemplate(ABC):

    def key_response(self):
        """
            Response to a keypress
        """

    def get_events(self):
        """
            Get a list of available events
        """

    def handle_event(self):
        """
            match methods to appropriate events
        """
