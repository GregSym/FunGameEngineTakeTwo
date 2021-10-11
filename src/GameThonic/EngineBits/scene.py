if __name__ == "__main__":
    from templates.scene_template import SceneTemplate
    from templates.object_template import ObjectTemplate
else:
    try:
        from .templates.scene_template import SceneTemplate
        from .templates.object_template import ObjectTemplate
    except ImportError:
        from templates.scene_template import SceneTemplate
        from templates.object_template import ObjectTemplate
    except ModuleNotFoundError:
        from gamethonic.enginebits.templates.scene_template import SceneTemplate
        from gamethonic.enginebits.templates.object_template import ObjectTemplate



from dataclasses import dataclass, field

import pygame


@dataclass
class Layer:
    objects: list[ObjectTemplate]

    def get_rect(self):
        """ gets a rect that wraps all items in layer """
        if len(self.objects) == 0:
            return pygame.Rect(100, 100, 200, 200)
        return pygame.Rect(
            min([object.get_rect().x for object in self.objects]),
            min([object.get_rect().y for object in self.objects]),
            max([object.get_rect().right for object in self.objects]),
            max([object.get_rect().bottom for object in self.objects])
        )


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
