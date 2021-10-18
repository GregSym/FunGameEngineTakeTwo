"""
# Physics Model, Controller & Handler
physics model and controller schemes for GameObjects to depend on
"""

from typing import Any, Callable, Optional
import pygame
from pygame.rect import Rect

from gamethonic.enginebits.templates import ObjectTemplate
try:
    from enginebits.templates import HandlerTemplate
    from enginebits.context import Context
except ModuleNotFoundError:
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
    max_velocity: Vector2 = Vector2(300, 300)
    acceleration: Vector2 = Vector2(0, 0)
    has_gravity: bool = False
    smooth_physics: bool = True
    """ smooths off the phsx bouncing effects """
    has_collision: bool = False
    collision: dict[direction.CollisionSide, ObjectTemplate] = field(default_factory=dict)

    @classmethod
    def from_rect(cls, rect: Rect):
        """ sets a physics model from a given rect type object """
        return cls(
            position=Vector2(rect.topleft),
            dimensions=Vector2(rect.width, rect.height)
        )

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
    on_collision: Optional[Callable[..., Any]] = None
    on_vertical_collision: Optional[Callable[..., Any]] = None
    on_horizontal_collision: Optional[Callable[..., Any]] = None
    on_bottom_collision: Optional[Callable[..., Any]] = None
    on_top_collision: Optional[Callable[..., Any]] = None
    on_right_collision: Optional[Callable[..., Any]] = None
    on_left_collision: Optional[Callable[..., Any]] = None


class CollisionHandler(HandlerTemplate):
    def __init__(self,
                 context: Context, model: PhysicsModelGeneric, target: str,
                 on_collision: CollisionInteraction = CollisionInteraction()) -> None:
        self.model = model
        self.on_collision = on_collision
        self.target = target
        self.context = context

    def get_collision(self, rect: Rect):
        """ higher-level get collision that composes lower functions as part of handler's update """
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

        if len((collisions := self.get_current_collision()).keys()) == 0:
            return

        self.model.collision = collisions

        handle_null(function=self.on_collision.on_collision)
        if (direction.CollisionSide.BOTTOM or direction.CollisionSide.TOP) in collisions.keys():
            handle_null(function=self.on_collision.on_vertical_collision)
            if direction.CollisionSide.BOTTOM in collisions:
                self.model.position.y = collisions[direction.CollisionSide.BOTTOM].get_rect().top - self.model.rect.height
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
            difference = self.model.rect.bottom - predicted_collision[direction.CollisionSide.BOTTOM].get_rect().top - 100
            self.model.max_velocity.y += difference if difference > 5 else 0
        elif direction.CollisionSide.TOP in predicted_collision:
            difference = self.model.rect.top - predicted_collision[direction.CollisionSide.TOP].get_rect().bottom - 100
            self.model.max_velocity.y += difference if difference > 5 else 0
        elif direction.CollisionSide.LEFT in predicted_collision:
            difference = self.model.rect.left - predicted_collision[direction.CollisionSide.LEFT].get_rect().right
            self.model.max_velocity.x += difference
        elif direction.CollisionSide.RIGHT in predicted_collision:
            difference = self.model.rect.right - predicted_collision[direction.CollisionSide.RIGHT].get_rect().left
            self.model.max_velocity.x += difference
        if len([key for key in predicted_collision.keys()]) == 0:
            self.model.max_velocity = Vector2(300, 300)
            return False
        return True

    def update(self):
        """ collects the relevant collisions and makes appropriate modifications to the physics_model """
        self.handle_predicted_collision()
        self.handle_collision()


class PhysicsHandler(HandlerTemplate):
    def __init__(self, context: Context, model: PhysicsModelGeneric) -> None:
        self.model = model
        self.context = context

    def apply_physics(self):
        self.model.velocity += self.model.acceleration * self.context.dt
        # remember to keep the directional stuff straight (or backwards, depending)
        velocity_directions = Vector2(self.model.velocity.x / abs(self.model.velocity.x) if self.model.velocity.x != 0 else 0,
                                      self.model.velocity.y / abs(self.model.velocity.y) if self.model.velocity.y != 0 else 0)
        # split pos into x, y additions because of min operation
        # if the vel is 0 then the direction is 0 so we can just let that sort itself out
        self.model.position += Vector2(
            velocity_directions.x * min(abs(self.model.velocity.x * self.context.dt), self.model.max_velocity.x),
            velocity_directions.y * min(abs(self.model.velocity.y * self.context.dt), self.model.max_velocity.y))

    def update(self):
        self.apply_physics()


class PhysicsController(controller_template.ControllerTemplate):
    """ Take two of physics controllers using handlers """

    def __init__(self, context: Context, physics_model: PhysicsModelGeneric = PhysicsModelGeneric()) -> None:
        self.context = context
        self.physics_model = physics_model
        self.handlers: list[HandlerTemplate] = [
            CollisionHandler(model=self.physics_model,
                             target='env', context=self.context,
                             on_collision=CollisionInteraction(on_vertical_collision=self.on_vertical_collision,
                                                               on_horizontal_collision=self.on_horizontal_collision,
                                                               on_bottom_collision=self.on_bottom_collision,
                                                               on_top_collision=self.on_top_collision,
                                                               on_left_collision=self.on_left_collision,
                                                               on_right_collision=self.on_right_collision))]
        self.physics_handler = PhysicsHandler(model=self.physics_model, context=self.context)
        self.handlers.append(self.physics_handler)

    def update(self):
        for handler in self.handlers:
            handler.update()

    def on_vertical_collision(self):
        if self.physics_model.smooth_physics:
            if 200 >= self.physics_model.velocity.y:
                self.physics_model.velocity.y = 0
            else:
                self.physics_model.velocity.y = self.physics_model.velocity.y * \
                    (-.9)
        else:
            self.physics_model.velocity.y = self.physics_model.velocity.y * \
                (-.9)

    def on_horizontal_collision(self):
        pass

    def on_bottom_collision(self):
        pass

    def on_top_collision(self):
        pass

    def on_right_collision(self):
        pass

    def on_left_collision(self):
        pass


class PlayerPhysics(PhysicsController):

    def on_vertical_collision(self):
        self.physics_model.velocity.y = 0


if __name__ == "__main__":
    print(asdict(PhysicsModelGeneric()))
