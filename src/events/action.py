import datetime
from datetime import time, timedelta, datetime
from typing import Any, Callable
from time import sleep
from enum import Enum, auto


class ActionState(Enum):
    """
        extends Enum

        record of possible states actions can take when being evaluated by an event-loop
    """
    DEFAULT = auto()
    DURATION = auto()
    TIME = auto()
    DELAY = auto()
    CONDITION = auto()
    DURATION_CONDITION = auto()


class Action:
    state = ActionState.DEFAULT

    def __init__(self, action: Callable) -> None:
        self.action = action

    @classmethod
    def do_until(self, action: Callable, duration: timedelta):
        self.state = ActionState.DURATION
        self.duration = duration
        self.end_time = datetime.now() + self.duration
        return self(action=action)

    @classmethod
    def do_at_time(self, action: Callable, time: datetime):
        self.state = ActionState.TIME
        self.time = time
        return self(action=action)

    @classmethod
    def do_after_delay(self, action: Callable, delay: timedelta):
        self.state = ActionState.DELAY
        self.delay = delay
        self.end_time = datetime.now() + self.delay
        return self(action=action)

    @classmethod
    def do_when(self, action: Callable, condition: Callable[..., bool]):
        self.state = ActionState.CONDITION
        self.condition = condition
        return self(action=action)

    @classmethod
    def do_until_condition(self, action: Callable, condition: Callable[..., bool]):
        self.state = ActionState.DURATION_CONDITION
        self.condition = condition
        return self(action=action)

    def update(self) -> bool:
        if self.state == ActionState.DURATION:
            if datetime.now() >= self.end_time:
                self.action()
                return True
            else:
                self.action()
                return False
        elif self.state == ActionState.TIME:
            if datetime.now().time() >= self.time:
                self.action()
                return True
            else:
                return False
        elif self.state == ActionState.DELAY:
            if datetime.now() >= self.end_time:
                self.action()
                return True
            return False
        elif self.state == ActionState.CONDITION:
            if self.condition():
                self.action()
                return True
            return False
        elif self.state == ActionState.DURATION_CONDITION:
            if self.condition():
                self.action()
                return True
            self.action()
            return False
        # default behaviour
        print('didn\'t pickup duration')
        self.action()
        return True


if __name__ == "__main__":

    def test_bool():
        return True

    event1 = Action.do_until(action=lambda: print("hi"),
                             duration=timedelta(seconds=2))
    print(event1.update())
    event2 = Action.do_at_time(action=lambda: print(
        "time"), time=time(hour=1, minute=2, second=8))
    print(event2.update())
    event3 = Action.do_after_delay(action=lambda: print(
        "delayed"), delay=timedelta(seconds=2))
    print(event3.update())
    event4 = Action.do_when(action=lambda: print(
        'condition'), condition=lambda _=None: test_bool())
    print(event4.update())
    event5 = Action.do_until_condition(action=lambda: print(
        'do while condition'), condition=lambda _=None: not test_bool())
    print(event5.update())
