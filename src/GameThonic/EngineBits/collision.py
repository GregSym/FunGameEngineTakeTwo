# std imports
from collections import deque
# local imports
from functions.direction import CollisionSide
from templates.object_template import ObjectTemplate


rough_collision_event: dict[CollisionSide, ObjectTemplate] = {}
collision_queue: deque[dict[CollisionSide, ObjectTemplate]] = deque([], maxlen=2)
