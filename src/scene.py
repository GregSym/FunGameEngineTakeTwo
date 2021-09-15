if __name__ == "__main__":
    from templates.scene_template import SceneTemplate
    from templates.object_template import ObjectTemplate
    from functions.direction import PhysxCalculations
else:
    try:
        from .templates.scene_template import SceneTemplate
        from .templates.object_template import ObjectTemplate
        from .functions.direction import PhysxCalculations
    except ImportError:
        from templates.scene_template import SceneTemplate
        from templates.object_template import ObjectTemplate
        from functions.direction import PhysxCalculations


from dataclasses import dataclass, field

@dataclass
class Layer:
    objects: list[ObjectTemplate]


@dataclass
class CollisionInfo:
    object: ObjectTemplate
    index: int
    angle: float

@dataclass
class CollisionObjects:
    """
        Last detected collision objects
    """
    vertical_object: list[ObjectTemplate] = field(default_factory=lambda: [])
    horizontal_object: list[ObjectTemplate] = field(default_factory=lambda: [])

@dataclass
class Scene(SceneTemplate):
    """
        Ideally this should instantiate a scene according to some rules?? This part I'm really not that sure about
        particularly with regards to efficiency.

        I guess we'll find out in like 48 hours when this thing is bigger and I can't remember where the problems 
        come from anymore
    """
    def __init__(self, scene: dict[str, Layer]) -> None:
        self.scene = scene
        super().__init__()


