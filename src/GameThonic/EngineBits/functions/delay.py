from time import time
from typing import Any, Callable


def time_delay(on_timer: Callable[..., Any], delay_length: float, start_time: float) -> bool:
    """ function for doing a time comparison and running a function on completion
        - returns true if the function has run
        - returns false in other cases
    """
    if time() - start_time >= delay_length:
        on_timer()
        return True
    return False
