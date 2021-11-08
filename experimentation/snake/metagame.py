from gamethonic.enginebits import Context
from gamethonic.enginebits.meta import MetaGame
from meta.metagame_interfaces import RuleInterface
import rules as rls


class SnakeMetaGame(MetaGame):

    def __init__(self, context: Context, rules: list[RuleInterface] = []) -> None:
        super().__init__(rules=rules)
        self.context = context
        self.rules = [
            rls.FoodRule(context=self.context)]
