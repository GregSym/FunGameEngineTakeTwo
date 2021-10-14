""" physics model and controller schemes for GameObjects to depend on """

from collections import deque
from typing import Any, Callable, Optional
import numpy as np
import pygame
from pygame.rect import Rect
try:
    from .models.collision import CollisionKeys, CollisionState
    from enginebits.templates.object_template import ObjectTemplate
    from enginebits.templates import HandlerTemplate
    from enginebits.context import Context
except ModuleNotFoundError:
    from gamethonic.enginebits.models.collision import CollisionKeys, CollisionState
    from gamethonic.enginebits.templates.object_template import ObjectTemplate
    from gamethonic.enginebits.templates import HandlerTemplate
    from gamethonic.enginebits.context import Context


if __name__ == "__main__":
    from templates import controller_template
else:
    try:
        from .templates import controller_template
    except ImportError:
        try:
            from templates import controller_template
        except ModuleNotFoundError:
            from gamethonic.enginebits.templates import controller_template

from gamethonic.enginebits.functions import direction
from dataclasses import asdict, dataclass, field
from pygame.math import Vector2


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

    @property
    def rect(self):
        """ Rect created from the physics_model's version of the rect
        - can be defined seperately from the sprite
        """
        return pygame.Rect(
            self.position.x,
            self.position.y,
            self.dimensions.x,
            self.dimensions.y
        )

    @rect.setter
    def rect(self, rect: pygame.Rect):
        self.position = Vector2(rect.x, rect.y)
        self.dimensions = Vector2(rect.width, rect.height)

    def predicted_rect(self, dt: float) -> pygame.Rect:
        """ Rect created if current velocity is added to position """
        return pygame.Rect(
            (predicted_position := self.position + self.velocity * dt).x,
            predicted_position.y,
            self.dimensions.x,
            self.dimensions.y)

    def projected_rect(self, dt: float) -> pygame.Rect:
        """ A large projection encompassing both the starting and predicted rect """
        return pygame.Rect(
            self.position.x, self.position.y,
            self.predicted_rect(dt=dt).right - self.position.x, self.predicted_rect(dt=dt).bottom - self.position.y
        )

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


@dataclass
class CollisionInteraction:
    on_vertical_collision: Optional[Callable[..., Any]] = None
    on_horizontal_collision: Optional[Callable[..., Any]] = None
    on_bottom_collision: Optional[Callable[..., Any]] = None
    on_top_collision: Optional[Callable[..., Any]] = None
    on_right_collision: Optional[Callable[..., Any]] = None
    on_left_collision: Optional[Callable[..., Any]] = None


class CollisionHandler(HandlerTemplate):
    def __init__(self,
                 model: PhysicsModelGeneric, 
                 target: str, 
                 context: Context, 
                 on_collision: CollisionInteraction = CollisionInteraction()) -> None:
        self.model = model
        self.on_collision = on_collision
        self.target = target
        self.context = context

    def get_collision(self, rect: Rect):
        return direction.PhysxCalculations.get_collision(
            rect=rect, target_rects={
                id: layer for (id, layer) in self.context.scene.items() if id == self.target
            }[self.target].objects,
            collision_function=direction.PhysxCalculations.collision_com
        )

    def get_current_collision(self):
        return self.get_collision(rect=self.model.rect)

    def get_predicted_collision(self):
        return self.get_collision(rect=self.model.predicted_rect(dt=self.context.dt))

    def get_projected_collision(self):
        return self.get_collision(rect=self.model.projected_rect(dt=self.context.dt))

    def handle_collision(self):
        """ handler for when a collision is currently being detected """
        def handle_null(function: Optional[Callable[..., Any]]):
            """ private: checks for null function names in CollisionInteraction struct """
            if function is None:
                return False
            function()
            return True
        if (direction.CollisionSide.BOTTOM or direction.CollisionSide.TOP) in (collisions := self.get_current_collision()).keys():
            handle_null(function=self.on_collision.on_vertical_collision)
            if direction.CollisionSide.BOTTOM in collisions:
                handle_null(function=self.on_collision.on_bottom_collision)
            elif direction.CollisionSide.TOP in collisions:
                handle_null(function=self.on_collision.on_top_collision)
        if (direction.CollisionSide.LEFT or direction.CollisionSide.RIGHT) in collisions.keys():
            handle_null(function=self.on_collision.on_horizontal_collision)
            if direction.CollisionSide.LEFT in collisions:
                handle_null(function=self.on_collision.on_left_collision)
            elif direction.CollisionSide.RIGHT in collisions:
                handle_null(function=self.on_collision.on_right_collision)
    
    def handle_predicted_collision(self):
        """ handler for when predicted collisions are detected, based on the physics of the item """
        if direction.CollisionSide.BOTTOM in (predicted_collision := self.get_predicted_collision()):
            difference = self.model.rect.bottom - predicted_collision[direction.CollisionSide.BOTTOM].get_rect().top
            self.model.position.y += difference
        elif direction.CollisionSide.TOP in predicted_collision:
            difference = self.model.rect.top - predicted_collision[direction.CollisionSide.BOTTOM].get_rect().bottom
            self.model.position.y += difference
        elif direction.CollisionSide.LEFT in predicted_collision:
            difference = self.model.rect.left - predicted_collision[direction.CollisionSide.BOTTOM].get_rect().right
            self.model.position.x += difference
        elif direction.CollisionSide.RIGHT in predicted_collision:
            difference = self.model.rect.right - predicted_collision[direction.CollisionSide.BOTTOM].get_rect().left
            self.model.position.x += difference
        if len([key for key in predicted_collision.keys()]) > 0:
            return True
        return False

    def update(self):
        """ collects the relevant collisions and makes appropriate modifications to the physics_model """
        self.handle_predicted_collision()
        self.handle_collision()


class PhysicsHandler(HandlerTemplate):
    def __init__(self, model: PhysicsModelGeneric, context: Context) -> None:
        self.model = model
        self.context = context


    def apply_physics(self):
        self.model.velocity += self.model.acceleration * self.context.dt
        self.model.position += self.model.velocity * self.context.dt


    def update(self):
        self.apply_physics()


class PhysicsController(controller_template.ControllerTemplate):

    detection_buffer = 10
    collision_target = 'env'
    collision: dict[CollisionKeys, ObjectTemplate] = {}
    collision_state = CollisionState.MOMENTUM
    collisions = deque[dict[direction.CollisionSide, ObjectTemplate]]

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
                angle = direction.PhysxCalculations.determineSide(
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
            self.handle_vertical_collision()
            self.collision.pop(CollisionKeys.VERTICAL)
        if CollisionKeys.HORIZONTAL in self.collision:
            self.handle_horizontal_collision()
            self.collision.pop(CollisionKeys.HORIZONTAL)

    def calculate_position(self):
        adjusted_velocity: dict[str, Vector2] = {}
        if CollisionKeys.VERTICAL in self.collision:  # vertical case
            adjusted_velocity['nullhack'] = Vector2(0, 0)
            if self.physics_model.velocity.y >= 0:
                # downwards
                # set can jump here
                adjusted_velocity['nullhack'].y = self.collision.pop(CollisionKeys.VERTICAL).get_rect(
                ).top - self.physics_model.rect.bottom
                self.set_jump()
            else:
                # upwards
                adjusted_velocity['nullhack'].y = self.physics_model.rect.top - \
                    self.collision.pop(
                        CollisionKeys.VERTICAL).get_rect().bottom

        # TODO: fix direction detection so that this logic works
        # if CollisionKeys.HORIZONTAL in self.collision:  # horizontal case
        #     if 'nullhack' not in adjusted_velocity:
        #         adjusted_velocity['nullhack'] = Vector2(0, 0)
        #     if self.physics_model.velocity.x >= 0:
        #         # downwards
        #         # set can jump here
        #         adjusted_velocity['nullhack'].x = self.physics_model.get_rect().right - \
        #             self.collision.pop(
        #                 CollisionKeys.HORIZONTAL).get_rect().left
        #     else:
        #         # upwards
        #         adjusted_velocity['nullhack'].x = self.physics_model.get_rect().left - \
        #             self.collision.pop(
        #                 CollisionKeys.HORIZONTAL).get_rect().right

        if 'nullhack' in adjusted_velocity:
            self.physics_model.position += adjusted_velocity.pop(
                'nullhack')
        else:
            self.physics_model.position += self.physics_model.velocity * self.context.dt

    def update(self):
        self.input()
        self.calculate_velocity()
        self.get_collision(self.physics_model.rect)
        self.handle_collision()
        self.get_collision(
            rect=self.physics_model.predicted_rect(dt=self.context.dt))
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
                self.physics_model.velocity.y = 0
            else:
                self.physics_model.velocity.y = self.physics_model.velocity.y * \
                    (-.9)
        else:
            self.physics_model.velocity.y = self.physics_model.velocity.y * \
                (-.9)

    def handle_horizontal_collision(self):
        pass

    def set_jump(self):
        pass


class PlayerPhysics(PhysicsController):

    def handle_vertical_collision(self):
        self.physics_model.velocity.y = 0
        self.set_jump()


if __name__ == "__main__":
    print(asdict(PhysicsModelGeneric()))
