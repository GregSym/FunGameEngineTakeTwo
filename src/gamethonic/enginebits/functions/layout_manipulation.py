from typing import Generator
from pygame.math import Vector2
from pygame.rect import Rect

class LayoutManipulation:

    @staticmethod
    def grid_from_container(container_rect: Rect, grid_width: int, grid_height: int) -> list[Vector2]:
        cell_width = container_rect.width / grid_width
        cell_height = container_rect.height / grid_height

        def _generate_row() -> Generator[Rect]:
            for i in range(cell_height):
                for j in range(cell_width):
                    yield Rect(container_rect.left + j*cell_width, container_rect.right + i*cell_height, cell_width, cell_height)
        
        cells: list[Rect] = list(_generate_row())