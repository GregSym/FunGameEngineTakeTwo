if __name__ == "__main__":
    from templates.scene_template import SceneTemplate
    from functions.direction import PhysxCalculations
    from models.collision import CollisionInfo
    from context import Context
    from object import Object
    from floor import Floor
else:
    from .templates.scene_template import SceneTemplate
    from .functions.direction import PhysxCalculations
    from .models.collision import CollisionInfo
    from .context import Context
    from .object import Object
    from .floor import Floor

from dataclasses import dataclass


@dataclass
class Layer:
    objects: list[Object]


class Scene(SceneTemplate):
    """
        Ideally this should instantiate a scene according to some rules?? This part I'm really not that sure about
        particularly with regards to efficiency.

        I guess we'll find out in like 48 hours when this thing is bigger and I can't remember where the problems 
        come from anymore
    """

    layers: list[Layer]

    def default_setup(self, context: Context):
        self.layers.append(Layer([Floor(context=context)]))

    def handle_collisions(self, obj: Object, lay: Layer):
        collision_indeces = obj.sprite.get_rect().collidelist(
            [object.sprite.get_rect() for object in lay.objects])
        print(collision_indeces)
        angle = PhysxCalculations.determineSide(
            obj, lay.objects[collision_indeces])  # not a good way to call that
        return CollisionInfo(
            object=lay.objects[collision_indeces],
            index=collision_indeces,
            angle=angle
        )

test_scene = Scene()