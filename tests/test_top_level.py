
import pygame
from gamethonic import main
import pytest


def test_top_level():
    """ runs through a single iteration of the event-loop, after setting up a defualt scene """
    engine = main.Engine()
    with pytest.raises(pygame.error):
        engine.loop_logic()
