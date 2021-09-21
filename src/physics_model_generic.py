
from .models.collision import CollisionKeys, CollisionKeysDetailed, CollisionState
from src.templates.object_template import ObjectTemplate
import numpy as np
from src.functions.direction import PhysxCalculations
import pygame
from src.context import Context
if __name__ == "__main__":
    from templates import controller_template
else:
    try:
        from .templates import controller_template
    except ImportError:
        from templates import controller_template


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
    dimensions: Vector2 = Vector2(50, 50)
    velocity: Vector2 = Vector2(0, 0)
    acceleration: Vector2 = Vector2(0, 0)
    has_gravity: bool = False
    smooth_physics: bool = True
    """ smooths off the phsx bouncing effects """
    has_collision: bool = False

    def get_rect(self):
        """ Rect created from the physics_model's version of the rect 
        - can be defined seperately from the sprite 
        """
        return pygame.Rect(
            self.position.x,
            self.position.y,
            self.dimensions.x,
            self.dimensions.y
        )

    def predicted_rect(self, dt: float) -> pygame.Rect:
        """ Rect created if current velocity is added to position """
        predicted_position = self.position + self.velocity * dt
        return pygame.Rect(predicted_position.x, predicted_position.y, self.dimensions.x, self.dimensions.y)

    def leading_edge(self, other_rect: pygame.Rect) -> Vector2:
        """ get the leading edges based on instantaneous velocity """
        if self.velocity.x >= 0:
            horizontal_edge = self.position.x + self.dimensions.x
        else:
            horizontal_edge = self.position.x
        if self.velocity.y >= 0:
            vertical_edge = self.position.y + self.dimensions.y
        else:
            vertical_edge = self.position.y
        return Vector2(horizontal_edge, vertical_edge)


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


class PhysicsController(controller_template.ControllerTemplate):

    detection_buffer = 10
    collision_target = 'env'
    collision: dict[CollisionKeys, ObjectTemplate] = {}
    collision_state = CollisionState.MOMENTUM

    def __init__(self, context: Context, physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        self.context = context
        self.physics_model = physics_model

    def get_collision(self, rect: pygame.Rect):
        if self.collision_target in self.context.scene:
            collision_layer = self.context.scene[self.collision_target]
            collision_objects = [
                object for object in collision_layer.objects if rect.colliderect(
                    object.get_rect().x, object.get_rect().y - 3, object.get_rect().right, object.get_rect().bottom)]
            for object in collision_objects:
                angle = PhysxCalculations.determineSide(
                    rect, object.get_rect())
                self.angle = angle
                if angle == np.pi / 2 or angle == 3 * np.pi / 2:
                    if CollisionKeys.VERTICAL not in self.collision:
                        self.collision[CollisionKeys.VERTICAL] = object
                else:
                    if CollisionKeys.HORIZONTAL not in self.collision:
                        self.collision[CollisionKeys.HORIZONTAL] = object
                if (CollisionKeys.VERTICAL in self.collision) and (CollisionKeys.HORIZONTAL in self.collision):
                    # reduces unecessary looping
                    return
        return

    def handle_collision(self):
        if CollisionKeys.VERTICAL in self.collision:
            self.collision.pop(CollisionKeys.VERTICAL)
        if CollisionKeys.HORIZONTAL in self.collision:
            self.collision.pop(CollisionKeys.HORIZONTAL)

    def calculate_position(self):
        adjusted_velocity: dict[str, Vector2] = {}
        if CollisionKeys.VERTICAL in self.collision:  # vertical case
            adjusted_velocity['nullhack'] = Vector2(0, 0)
            if self.physics_model.velocity.y >= 0:
                # downwards
                # set can jump here
                adjusted_velocity['nullhack'].y = self.physics_model.get_rect().bottom - \
                    self.collision[CollisionKeys.VERTICAL].get_rect().top
            else:
                # upwards
                adjusted_velocity['nullhack'].y = self.physics_model.get_rect().top - \
                    self.collision[CollisionKeys.VERTICAL].get_rect().bottom
            self.collision.pop(CollisionKeys.VERTICAL)
        if CollisionKeys.HORIZONTAL in self.collision:  # horizontal case
            if 'nullhack' not in adjusted_velocity:
                adjusted_velocity['nullhack'] = Vector2(0, 0)
            if self.physics_model.velocity.x >= 0:
                # downwards
                # set can jump here
                adjusted_velocity['nullhack'].x = self.physics_model.get_rect().right - \
                    self.collision[CollisionKeys.HORIZONTAL].get_rect().left
            else:
                # upwards
                adjusted_velocity['nullhack'].x = self.physics_model.get_rect().left - \
                    self.collision[CollisionKeys.HORIZONTAL].get_rect().right
            self.collision.pop(CollisionKeys.HORIZONTAL)
        if 'nullhack' in adjusted_velocity:
            self.physics_model.position += adjusted_velocity
            adjusted_velocity.pop('nullhack')
        else:
            self.physics_model.position += self.physics_model.velocity * self.context.dt



    def update(self):
        self.input()
        self.calculate_velocity()
        self.get_collision(current_rect := self.physics_model.get_rect())
        self.handle_collision()
        self.get_collision(
            rect=(predicted_rect := self.physics_model.predicted_rect(dt=self.context.dt)))
        self.physics_model.position = self.physics_model.velocity * self.context.dt
        self.calculate_position()

    def input(self):
        pass

    def calculate_velocity(self):
        self.physics_model.velocity += self.physics_model.acceleration * self.context.dt

    def gravity_update(self, dt: float):
        if self.physics_model.has_gravity:
            self.physics_model.velocity += self.physics_model.acceleration * dt
            self.physics_model.position += self.physics_model.velocity * dt

    def handle_vertical_collision(self):
        if self.physics_model.smooth_physics:
            if self.physics_model.acceleration.y >= self.physics_model.velocity.y:
                self.velocity.y = 0
            else:
                self.physics_model.velocity.y = self.physics_model.velocity.y * \
                    (-.9)
        else:
            self.physics_model.velocity.y = self.physics_model.velocity.y * \
                (-.9)

    def handle_horizontal_collision(self):
        pass


class PlayerPhysics(PhysicsModelGeneric):
    def handle_vertical_collision(self):
        self.velocity.y = 0


if __name__ == "__main__":
    print(asdict(PhysicsModelGeneric()))
