from typing import Generator
from pygame.rect import Rect


class LayoutManipulation:

    @staticmethod
    def grid_from_container(container_rect: Rect, grid_width: int, grid_height: int) -> Generator[Rect, None, None]:
        """ generates a grid from a given surface for specified dimensions """
        cell_width = int(container_rect.width / grid_width)
        cell_height = int(container_rect.height / grid_height)

        for i in range(cell_height):
            for j in range(cell_width):
                yield Rect(container_rect.left + j*cell_width, container_rect.right + i*cell_height, cell_width, cell_height)
