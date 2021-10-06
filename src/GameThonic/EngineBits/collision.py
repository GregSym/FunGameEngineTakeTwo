# std imports
from collections import deque
# local imports
from EngineBits.context import Context
from functions.direction import CollisionSide
from templates.object_template import ObjectTemplate


rough_collision_event = dict[CollisionSide, ObjectTemplate]
collision_queue = deque[dict[CollisionSide, ObjectTemplate]]

class CollisionHandler:
    def __init__(self, context: Context) -> None:
        self.context = context
    
    
    def process_collisions(self):
        for layer in self.context.scene.values():
            for object in layer.objects:
                if object.model.has_collision:
                    pass