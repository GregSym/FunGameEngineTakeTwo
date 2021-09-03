from pygame import Surface, Vector2
if __name__ == "__main__":
    from object import Object
    from context import Context
    from physics_model_generic import PhysicsModelGeneric
else:
    from .object import Object
    from .context import Context
    from .physics_model_generic import PhysicsModelGeneric


class Floor(Object):

    def __init__(
            self,
            context: Context,
            dimensions: Vector2 = Vector2(50, 50),
            physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__(context, dimensions=dimensions, physics_model=physics_model)
        self.position.x = 0  # force pos 0
        # reset sprite assignment of floor to this full screen width object
        self.sprite = Surface(
            size=(self.context.surface_info.width, self.dimensions.y))
