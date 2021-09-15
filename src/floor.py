from pygame import Surface, Vector2
from . import object
from . import context
from . import physics_model_generic


class Floor(object.Object):

    def __init__(
            self,
            context: context.Context,
            dimensions: Vector2 = Vector2(50, 50),
            physics_model: physics_model_generic.PhysicsModelGeneric = physics_model_generic.PhysicsModelGeneric()
    ) -> None:
        super().__init__(context, dimensions=dimensions, physics_model=physics_model)
        self.physics_model.position.x = 0  # force pos 0
        # reset sprite assignment of floor to this full screen width object
        self.sprite = Surface(
            size=(self.context.surface_info.width, self.dimensions.y))
        self.rect = self.sprite.get_rect()
        self.collision_target = ''
