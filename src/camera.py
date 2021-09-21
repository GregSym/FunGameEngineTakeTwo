import pygame
from pygame.math import Vector2
from src.scene import Layer
from .templates.event_loop_item import EventLoopItem
from .context import Context

class Camera(EventLoopItem):

    buffer_size = 100
    tracking_velocity = 300

    def __init__(self, context: Context, target: str) -> None:
        super().__init__()
        self.context = context
        self.target = target
        self.layer = self.setup() # get layer to track in setup
        self.tracked_rect = pygame.Rect()

    def target_position(self) -> Vector2:
        return Vector2(
            self.tracked_rect.x,
            self.tracked_rect.y
        )
    
    def setup(self):
        # define buffer
        self.buffer = pygame.Rect(
            self.buffer_size,
            self.buffer_size,
            self.context.screen.get_size()[0] + self.buffer_size,
            self.context.screen.get_size()[1] + self.buffer_size
        )

        # define target
        for layer_key in self.context.scene.keys():
            if layer_key == self.target:
                return self.context.scene[layer_key]
        return Layer()

    def update(self):
        if self.target_position().x >= self.buffer.right:
            self.track(direction=Vector2(1, 0))
        elif self.target_position().x < self.buffer.left:
            self.track(direction=Vector2(-1, 0))
        if self.target_position().y >= self.buffer.bottom:
            self.track(direction=Vector2(0, 1))
        elif self.target_position().y < self.buffer.y:
            self.track(direction=Vector2(0, -1))

    def track(self, direction: Vector2):
        for layer in self.context.scene.values():
            for object in layer.objects:
                object.adjust_position(adjustment=self.tracking_velocity * direction)


