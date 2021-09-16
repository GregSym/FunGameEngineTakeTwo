
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
    has_collision: bool = False

    def gravity_update(self, dt: float):
        if self.has_gravity:
            self.velocity += self.acceleration * dt
            self.position += self.velocity * dt

    def handle_vertical_collision(self):
        if self.smooth_physics:
            if self.acceleration.y >= self.velocity.y:
                self.velocity.y = 0
            else:
                self.velocity.y = self.velocity.y * \
                    (-.9)
        else:
            self.velocity.y = self.velocity.y * \
                (-.9)

    def handle_horizontal_collision(self):
        pass

class PlayerPhysics(PhysicsModelGeneric):
    def handle_vertical_collision(self):
        self.velocity.y = 0


if __name__ == "__main__":
    print(asdict(PhysicsModelGeneric()))
