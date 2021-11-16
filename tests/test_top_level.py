
from gamethonic import Engine


def test_top_level():
    """ runs through a single iteration of the event-loop, after setting up a defualt scene """
    engine = Engine()
    engine.setup()
    engine.loop_logic()
