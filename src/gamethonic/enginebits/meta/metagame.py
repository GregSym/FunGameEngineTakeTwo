
import metagame_interfaces


class MetaGame:

    def __init__(self, rules: list[metagame_interfaces.RuleInterface] = []) -> None:
        self.rules: list[metagame_interfaces.RuleInterface] = rules
    
    def handle_rules(self):
        for rule in self.rules:
            rule.check_rule()
    
    def update(self):
        """ entrypoint for game rules at a middle level in the game engine """
        self.handle_rules()