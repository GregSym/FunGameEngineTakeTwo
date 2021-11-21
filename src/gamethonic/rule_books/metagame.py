
from typing import Protocol


class MetaGame(Protocol):
    """ An interface for game rules and procedures at the top level
        - analyses stuff like basic layouts (for games that use grid systems)
        - calculates score
        - can be used to control positioning of GameObjects as an alternative
        to physics driven positioning - _ideally_ one wouldn't handle physics
        in this particular abstraction but it should be possible to do, from
        a design goal perspective
    """

    def checkEventsList(self):
        ...
