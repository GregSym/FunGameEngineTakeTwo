
from meta.metagame_interfaces import RuleInterface


class MetaGame:

    def __init__(self, rules: list[RuleInterface] = []) -> None:
        self.rules: list[RuleInterface] = rules
    
    def handle_rules(self):
        for rule in self.rules:
            rule.check_rule()
    
    def update(self):
        self.handle_rules()