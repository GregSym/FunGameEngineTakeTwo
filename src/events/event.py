from datetime import timedelta

class Event:
    def __init__(self, action: function) -> None:
        self.action = action
        
    @classmethod
    def do_until(self, action: function, duration: timedelta):
        self.duration = duration
        return self(action=action)