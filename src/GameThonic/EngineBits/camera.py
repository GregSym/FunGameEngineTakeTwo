from pygame.math import Vector2
from pygame.rect import Rect
from gamethonic.enginebits import Layer
from gamethonic.enginebits.templates import EventLoopItem
from gamethonic.enginebits import Context


class Camera(EventLoopItem):

    buffer_size = 300
    tracking_velocity = 150

    def __init__(self, context: Context, target: str = 'player') -> None:
        super().__init__()
        self.context = context
        self.target = target
        self.layer = self.setup()  # get layer to track in setup
        self.tracked_rect = self.layer.get_rect()

    def target_position(self) -> Vector2:
        return Vector2(
            self.tracked_rect.x,
            self.tracked_rect.y
        )

    def setup(self):
        # define buffer
        self.buffer = Rect(
            self.buffer_size,
            self.buffer_size,
            self.context.screen.get_size()[0] - self.buffer_size,
            self.context.screen.get_size()[1] - self.buffer_size
        )

        # define target
        for layer_key in self.context.scene.keys():
            if layer_key == self.target:
                return self.context.scene[layer_key]
        return Layer(objects=[])

    def update(self):
        self.tracked_rect = self.layer.get_rect()
        if self.tracked_rect.x >= self.buffer.right:
            self.track(direction=Vector2(1, 0))
        elif self.tracked_rect.right < self.buffer.left:
            self.track(direction=Vector2(-1, 0))
        if self.tracked_rect.y >= self.buffer.bottom:
            self.track(direction=Vector2(0, 1))
        elif self.tracked_rect.bottom < self.buffer.y:
            self.track(direction=Vector2(0, -1))

    def track(self, direction: Vector2):
        for layer in self.context.scene.values():
            for object in layer.objects:
                object.adjust_position(adjustment=self.layer.objects[0].get_velocity(
                ).magnitude() * 2 * direction * (-1))

    def loop_logic(self):
        pass

    def draw(self):
        pass
