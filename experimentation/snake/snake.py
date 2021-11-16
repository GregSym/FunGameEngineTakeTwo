from gamethonic import Engine
from gamethonic.enginebits import Layer, PhysicsModelGeneric
from pc_snake import Snake
from food import Food
import metagame as mg


def snake():
    engine = Engine()
    engine.setup()
    engine.context.scene = {
        "snake": Layer(objects=[Snake(context=engine.context)]),
        "food": Layer(objects=[Food(context=engine.context, physics_model=PhysicsModelGeneric())]),
        "env": Layer(objects=[])
    }
    engine.metagame = mg.SnakeMetaGame(context=engine.context)
    engine.run()

if __name__ == "__main__":
    raise SystemExit(snake())
