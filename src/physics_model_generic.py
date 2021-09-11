
from dataclasses import asdict, dataclass
from pygame import Vector2


@dataclass
class PhysicsModelGeneric:
    """
        Super-basic, generic physics model
        - pos @ origin, no velocity, no gravity/horizontal acc.
    """
    position: Vector2 = Vector2(0, 0)
    """ Position of the top left-hand corner of the associated sprite """
    velocity: Vector2 = Vector2(0, 0)
    acceleration: Vector2 = Vector2(0, 0)
    has_gravity: bool = False
    smooth_physics: bool = True
    """ smooths off the phsx bouncing effects """

    def gravity_update(self, dt: float):
        if self.has_gravity:
            self.position += self.velocity * dt
            self.velocity += self.acceleration * dt


if __name__=="__main__":
    print(asdict(PhysicsModelGeneric()))