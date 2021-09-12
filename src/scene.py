if __name__ == "__main__":
    from templates.scene_template import SceneTemplate
    from functions.direction import PhysxCalculations
    from context import Context
    from object import Object
    from floor import Floor
else:
    try:
        from .templates.scene_template import SceneTemplate
        from .functions.direction import PhysxCalculations
        from .context import Context
        from .object import Object
        from .floor import Floor
    except ImportError:
        from templates.scene_template import SceneTemplate
        from functions.direction import PhysxCalculations
        from context import Context
        from object import Object
        from floor import Floor


from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Layer:
    id: str
    objects: list[Object]
    has_collision: bool = False
    collides_with: list[str] = field(default_factory=lambda: [])


@dataclass
class CollisionInfo:
    object: Object
    index: int
    angle: float


class Scene(SceneTemplate):
    """
        Ideally this should instantiate a scene according to some rules?? This part I'm really not that sure about
        particularly with regards to efficiency.

        I guess we'll find out in like 48 hours when this thing is bigger and I can't remember where the problems 
        come from anymore
    """

    layers: list[Layer] = []

    def default_setup(self, context: Context):
        env_layer = Layer([Floor(context=context)])
        self.layers.append(
            env_layer
        )

    def layer_interaction(self):
        for layer in self.layers:
            if layer.has_collision:
                target_layers = []
                for target_name in layer.collides_with:
                    target_layers.append(
                        [lay for lay in self.layers if lay.id == target_name][0])
                for item in layer.objects:
                    for lay in target_layers:
                        self.handle_collisions(obj=item, lay=lay)

    def handle_collisions(self, obj: Object, lay: Layer):
        collision_indeces = obj.rect.collidelist(
            [object.rect for object in lay.objects])
        print(collision_indeces)
        angle = PhysxCalculations.determineSide(
            obj.rect, lay.objects[collision_indeces].rect)  # not a good way to call that
        obj.set_collision(
            collision=CollisionInfo(
                object=lay.objects[collision_indeces],
                index=collision_indeces,
                angle=angle
            )
        )
        return CollisionInfo(
            object=lay.objects[collision_indeces],
            index=collision_indeces,
            angle=angle
        )

    def update(self):
        self.layer_interaction()
        for layer in self.layers:
            for object in layer.objects:
                object.update()

    def draw(self):
        for layer in self.layers:
            for object in layer.objects:
                object.draw()

    def __for_every_object(self, func: Callable):
        for layer in self.layers:
            for object in layer.objects:
                func()


test_scene = Scene()
