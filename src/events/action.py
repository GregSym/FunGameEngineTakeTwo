import datetime
from datetime import time, timedelta, datetime
from typing import Callable
from time import sleep


class Action:
    mode = "default"

    def __init__(self, action: Callable) -> None:
        self.action = action

    @classmethod
    def do_until(self, action: Callable, duration: timedelta):
        self.mode = "duration"
        self.duration = duration
        self.end_time = datetime.now() + self.duration
        return self(action=action)

    @classmethod
    def do_at_time(self, action: Callable, time: datetime):
        self.mode = "time"
        self.time = time
        return self(action=action)

    @classmethod
    def do_after_delay(self, action: Callable, delay: timedelta):
        self.mode = "delay"
        self.delay = delay
        self.end_time = datetime.now() + self.delay
        return self(action=action)

    def update(self) -> bool:
        if self.mode == 'duration':
            if datetime.now() >= self.end_time:
                self.action()
                return True
            else:
                self.action()
                return False
        elif self.mode == 'time':
            if datetime.now().time() >= self.time:
                self.action()
                return True
            else:
                return False
        elif self.mode == "delay":
            if datetime.now() >= self.end_time:
                self.action()
                return True
            return False
        print('didn\'t pickup duration')
        self.action()
        return True


if __name__ == "__main__":
    event1 = Action.do_until(action=lambda: print("hi"),
                            duration=timedelta(seconds=2))
    print(event1.update())
    event2 = Action.do_at_time(action=lambda: print(
        "time"), time=time(hour=1, minute=2, second=8))
    print(event2.update())
    event3 = Action.do_after_delay(action=lambda: print(
        "delayed"), delay=timedelta(seconds=2))
    print(event3.update())
