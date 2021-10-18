from gamethonic.enginebits.events import Action
import datetime


def test_actions_factory():
    def test_bool() -> bool:
        return True

    event1 = Action.do_until(action=lambda: print("hi"),
                             duration=datetime.timedelta(seconds=2))
    assert not event1.update()
    event1_do_now = Action.do_until(action=lambda: print("hi"), duration=datetime.timedelta(seconds=0))
    assert event1_do_now.update()
    event2 = Action.do_at_time(action=lambda: print(
        "time"), time=datetime.time(hour=1, minute=2, second=8))
    assert (not event2.update()) or (datetime.datetime.now().time() == datetime.time(hour=1, minute=2, second=8) and event2.update())
    event3 = Action.do_after_delay(action=lambda: print(
        "delayed"), delay=datetime.timedelta(seconds=2))
    assert not event3.update()
    event4 = Action.do_when(action=lambda: print(
        'condition'), condition=lambda _=None: test_bool())
    assert event4.update()
    assert event4.condition()
    event5 = Action.do_until_condition(action=lambda: print(
        'do while condition'), condition=lambda _=None: not test_bool())
    assert not event5.update()
