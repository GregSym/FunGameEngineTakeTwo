from gamethonic.enginebits import Context
import pc_snake
import food


class SnakeMetaGame:


    def __init__(self, context: Context) -> None:
        self.context = context
        self.snake: pc_snake.Snake = pc_snake.Snake.of(context=self.context)
        self.food: food.Food = food.Food.of(context=self.context)