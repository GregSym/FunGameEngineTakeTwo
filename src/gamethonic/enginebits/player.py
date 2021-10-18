"""
    Module pertaining to a rough mock-up of a player object
"""
if __name__ == "__main__":
    from object import Object
    from context import Context
    from physics_model_generic import PhysicsModelGeneric
    from constants.colours import Colours
    from player_controller import PlayerController
else:
    try:
        from .object import Object
        from .context import Context
        from .physics_model_generic import PhysicsModelGeneric
        from .constants.colours import Colours
        from .player_controller import PlayerController
    except ImportError:
        try:
            from enginebits.object import Object
            from enginebits.context import Context
            from enginebits.physics_model_generic import PhysicsModelGeneric
            from enginebits.constants.colours import Colours
            from enginebits.player_controller import PlayerController
        except ModuleNotFoundError:
            from gamethonic.enginebits.object import Object
            from gamethonic.enginebits.context import Context
            from gamethonic.enginebits.physics_model_generic import PhysicsModelGeneric
            from gamethonic.enginebits.constants.colours import Colours
            from gamethonic.enginebits.player_controller import PlayerController
    except ModuleNotFoundError:
        from gamethonic.enginebits.object import Object
        from gamethonic.enginebits.context import Context
        from gamethonic.enginebits.physics_model_generic import PhysicsModelGeneric
        from gamethonic.enginebits.constants.colours import Colours
        from gamethonic.enginebits.player_controller import PlayerController


import numpy as np


class Player(Object):
    def __init__(self,
                 context: Context,
                 physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__(context, physics_model=physics_model)
        self.sprite.fill(color=Colours.blue)
        self.max_velocity = 500
        self.controller = PlayerController(
            context=self.context, physics_model=self.physics_model)  # set a controller

    def collision_interacting_event(self):
        self.controller.update()
