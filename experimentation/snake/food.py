from gamethonic.enginebits import Context
from gamethonic.enginebits import Object
from gamethonic.enginebits import PhysicsModelGeneric

class Food(Object):
    """ GameObject repr of food """

    def __init__(self, context: Context, physics_model: PhysicsModelGeneric) -> None:
        super().__init__(context, physics_model=physics_model)