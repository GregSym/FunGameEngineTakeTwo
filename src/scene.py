if __name__ == "__main__":
    from templates.scene_template import SceneTemplate
    from templates.object_template import ObjectTemplate as Object
    from functions.direction import PhysxCalculations
else:
    from .templates.scene_template import SceneTemplate
    from .templates.object_template import ObjectTemplate as Object
    from .functions.direction import PhysxCalculations


from dataclasses import dataclass


@dataclass
class Layer:
    objects: list[Object]


@dataclass
class CollisionInfo:
    object: Object
    index: int
    angle: float

@dataclass
class Scene(SceneTemplate):
    """
        Ideally this should instantiate a scene according to some rules?? This part I'm really not that sure about
        particularly with regards to efficiency.

        I guess we'll find out in like 48 hours when this thing is bigger and I can't remember where the problems 
        come from anymore
    """

    scene: dict[str, Layer]

    def handle_collisions(self, obj: Object, lay: Layer):
        pass


test_scene = Scene()
