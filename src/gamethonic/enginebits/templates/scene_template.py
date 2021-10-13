from abc import ABC


class SceneTemplate(ABC):
    """
        Abstract Base Class of a controller object for handling tasks that need to be applied
        to large numbers of items in a scene, systematically
    """

    def setup(self):
        """
            Setup the objects in the scene
        """

    def handle_collisions(self):
        """
            Handles collisions between target objects and selected layers
        """

    def camera_motion(self):
        """
            Handles the motion of the camera
        """
