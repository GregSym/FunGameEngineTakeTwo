

from typing import Protocol


class RuleInterface(Protocol):
    """ An interface for GameRule behaviour as expected by the MetaGame class that uses them """

    def rule_has_event(self) -> bool:
        """ does this rule have an event to act upon """

    def on_rule_applicable(self):
        """ action to perform when rule_has_event returns True """

    def check_rule(self):
        """ entrypoint to be called in the event loop """


class MetaGameInterface(Protocol):
    """ Interface for the object that sits at the middle level of the engine, implementing 'Game Rules' """

    def handle_rules(self):
        """ check the rules of the game and act on them """

    def update(self):
        """ standard update method for interaction with engine """
