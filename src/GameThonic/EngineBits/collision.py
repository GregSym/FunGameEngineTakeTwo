from functions.direction import CollisionSide
from templates.object_template import ObjectTemplate
from collections import deque


rough_collision_event = dict[CollisionSide, ObjectTemplate]
collision_queue = deque[dict[CollisionSide, ObjectTemplate]]