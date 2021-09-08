if __name__=="__main__":
    from templates.scene_template import SceneTemplate
    from object import Object
else:
    from .templates.scene_template import SceneTemplate
    from .object import Object
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

    def handle_collisions(self, obj, lay):
        for layer in self.layers:
            if layer is lay:
                for object in layer.objects:
                    object.test_collision(obj)
