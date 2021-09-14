from pygame import Surface, Vector2
if __name__ == "__main__":
    from object import Object
    from context import Context
    from physics_model_generic import PhysicsModelGeneric
else:
    try:
        from .object import Object
        from .context import Context
        from .physics_model_generic import PhysicsModelGeneric
    except ImportError:
        from object import Object
        from context import Context
        from physics_model_generic import PhysicsModelGeneric



class Floor(Object):

    def __init__(
            self,
            context: Context,
            dimensions: Vector2 = Vector2(50, 50),
            physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        super().__init__(context, dimensions=dimensions, physics_model=physics_model)
        self.physics_model.position.x = 0  # force pos 0
        # reset sprite assignment of floor to this full screen width object
        self.sprite = Surface(
            size=(self.context.surface_info.width, self.dimensions.y))
        self.rect = self.sprite.get_rect()

    def draw(self):
        super().draw()
        self.rect.update(self.physics_model.position.x, self.physics_model.position.y, self.context.surface_info.width, self.dimensions.y)
