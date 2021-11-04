from gamethonic import Engine
from gamethonic.enginebits import Layer
from pc_snake import Snake
from food import Food


def snake():
    engine = Engine()
    engine.context.scene = {
        "snake": Layer(objects=[Snake()]),
        "food": Layer(objects=[Food()]),
        "env": Layer(objects=[])
    }
    engine.run()

if __name__ == "__main__":
    raise SystemExit(snake())
