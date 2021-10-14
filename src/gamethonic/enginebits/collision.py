# std imports
from collections import deque
# local imports
try:
    from functions.direction import CollisionSide
    from templates.object_template import ObjectTemplate
except ImportError:
    try:
        from enginebits.functions.direction import CollisionSide
        from enginebits.templates.object_template import ObjectTemplate
    except ModuleNotFoundError:
        from gamethonic.enginebits.functions.direction import CollisionSide
        from gamethonic.enginebits.templates.object_template import ObjectTemplate


rough_collision_event: dict[CollisionSide, ObjectTemplate] = {}
collision_queue: deque[dict[CollisionSide, ObjectTemplate]] = deque([], maxlen=2)
