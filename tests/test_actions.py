from gamethonic.enginebits.events import Action
import datetime

def test_actions_factory():
    def test_bool() -> bool:
        return True

    event1 = Action.do_until(action=lambda: print("hi"),
                             duration=datetime.timedelta(seconds=2))
    assert event1.update() == False
    event2 = Action.do_at_time(action=lambda: print(
        "time"), time=datetime.time(hour=1, minute=2, second=8))
    assert event2.update() == False or (datetime.datetime.now() == datetime.time(hour=1, minute=2, second=8) and event2.update() == True)
    event3 = Action.do_after_delay(action=lambda: print(
        "delayed"), delay=datetime.timedelta(seconds=2))
    assert event3.update() == False
    event4 = Action.do_when(action=lambda: print(
        'condition'), condition=lambda _=None: test_bool())
    assert event4.update() == True
    event5 = Action.do_until_condition(action=lambda: print(
        'do while condition'), condition=lambda _=None: not test_bool())
    assert event5.update() == False
