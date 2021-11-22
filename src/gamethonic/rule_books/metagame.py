
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
    score: int = 0
    """ returns score as evaluated by the metagame """
    level: int = 0

    def update(self):
        """ update evaluation of the MetaGame """
