import abc
from typing import Any, Callable
from gamethonic.enginebits.context import Context
from gamethonic.enginebits.events import Action


class ContinuouActionTemplate(abc.ABC):
    """ A rough outline of a class that uses the events.Action class to avoid turning on the special
        event handler mode that allows pygame to register held keypresses, as it behaves weirdly and
        has lots of warnings
    """

    @abc.abstractmethod
    def action_is_done(self) -> bool:
        """ returns True when the action is intended to cease """

    @abc.abstractmethod
    def run_with_updates(self):
        """ runs an initial action followed by a separate repeated action for the duration of the keystroke
            - relies on the Action class that triggers events higher up the event loop
            - communicates through a link to the app's Context
        """

    @abc.abstractmethod
    def run_with_updates_declarative(self, init_action: Callable[..., Any], during_action: Callable[..., Any]):
        """ a version of run with updates that accepts functions to run, rather than allowing an override of extent methods
            of this class
        """


class ContinuousActionImplementation(ContinuouActionTemplate):
    """ An implementation of the funcionality implied by the ContinuousActionTemplate class """
    def __init__(self, context: Context) -> None:
        self.context = context
        self.held_cycles = 0
        self.done = False
        """ variable tracking completion of button press """

    def action_is_done(self) -> bool:
        return self.done

    def init_action(self):
        """ action that gets run on initial keypress """

    def during_action(self):
        """ Action that gets run between the downpress and the release """

    def end_action(self):
        """ Action to call on the release of the key / keyup event """
        self.done = True

    def run_with_updates(self):
        if self.held_cycles == 0:
            self.held_cycles += 1
            self.init_action()
        self.context.add_action(action=Action.do_until_condition(action=self.during_action, condition=self.action_is_done))

    def run_with_updates_declarative(self, init_action: Callable[..., Any], during_action: Callable[..., Any], **terminators: Callable[..., bool]):
        if self.held_cycles == 0:
            self.held_cycles += 1
            init_action()
        conditions: list[Callable[..., bool]] = [self.action_is_done]
        for terminator in terminators.values():
            conditions.append(terminator)
        self.context.add_action(action=Action.do_until_condition(
            action=during_action, condition=lambda _=None: any([condition() for condition in conditions])))
