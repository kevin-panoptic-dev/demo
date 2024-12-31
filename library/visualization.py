import pygame
import sys
import os
from typing import NoReturn
from pygame.time import Clock

pygame.font.init()


class graphics:
    @staticmethod
    def inbutton(
        mouse_position: tuple[int, int],
        button_position: tuple[float, float, float, float],
    ) -> bool:
        if (
            button_position[0]
            < mouse_position[0]
            < button_position[0] + button_position[2]
        ) and (
            button_position[1]
            < mouse_position[1]
            < button_position[0] + button_position[3]
        ):
            return True
        return False

    @staticmethod
    def terminate() -> NoReturn:
        pygame.quit()
        sys.exit()

    @staticmethod
    def init(
        window_size: tuple, caption: str = "game", fps: int = 60
    ) -> tuple[pygame.Surface, Clock]:
        if not isinstance(caption, str) or not isinstance(fps, int):
            raise pygame.error("Invalid type for optional parameters.")
        if not isinstance(window_size, tuple) or len(window_size) != 2:
            raise pygame.error("Invalid window size.")
        if not isinstance(window_size[0], int) or not isinstance(window_size[1], int):
            raise pygame.error("Invalid type inside window size.")
        pygame.init()
        pygame.font.init()
        window: pygame.Surface = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()
        pygame.display.set_caption(caption)
        return window, clock

    @staticmethod
    def load(path: list[str], *, resize: tuple[int, int] | None = None):
        if not isinstance(path, list) or not all(
            isinstance(element, str) for element in path
        ):
            raise pygame.error("Invalid path.")
        if (not isinstance(resize, tuple) or len(resize) != 2) and resize is not None:
            raise pygame.error("Invalid image size.")
        if resize is not None and (
            not isinstance(resize[0], int) or not isinstance(resize[1], int)
        ):
            raise pygame.error("Invalid type inside image size.")

        raw_image = pygame.image.load(os.path.join(*path))
        final_image = (
            pygame.transform.scale(raw_image, resize)
            if resize is not None
            else raw_image
        )
        return final_image

    @staticmethod
    def create_font(size: int, *, name: str = "comicsans"):
        if not isinstance(size, int) or not isinstance(name, str):
            raise pygame.error("Invalid input type for font initialization.")
        return pygame.font.SysFont(name, size)

    @staticmethod
    def render_button(
        window: pygame.Surface,
        text: str,
        size: tuple[int, int, int, int],
        font: pygame.font.Font = pygame.font.SysFont("comiscans", 40),
        font_color: tuple[int, int, int] = (65, 65, 65),
        button_color: tuple[int, int, int] = (161, 227, 168),
    ):
        button = pygame.Rect(*size)
        label = font.render(text, 1, font_color)
        font_x = int(size[0] + size[2] / 2 - label.get_width() / 2)
        font_y = int(size[1] + size[3] / 2 - label.get_height() / 2)
        pygame.draw.rect(window, button_color, button, border_radius=int(size[2] / 8))
        window.blit(label, (font_x, font_y))

    @staticmethod
    def create_screen(
        window: pygame.Surface,
        background: pygame.Surface | tuple[int, int, int] = (205, 192, 190),
        *,
        title_font: pygame.font.Font = pygame.font.SysFont("comiscans", 60),
        font_color: tuple[int, int, int] = (65, 65, 65),
        title_text: list[tuple[str, tuple[int, int]]] = [],
        button_font: pygame.font.Font = pygame.font.SysFont("comiscans", 30),
        button_color: tuple[int, int, int] = (161, 227, 168),
        buttons: list[tuple[str, tuple[int, int, int, int]]] = []
    ) -> None:
        """
        Create a simple, text-based screen with button rendered
        (event check isn't be implemented)

        Args:
            window (pygame.Surface): Window Background
            background (pygame.Surface | tuple[int, int, int], optional):
            Items used to fill background.
            Defaults to (205, 192, 190).

            title_font (pygame.font.Font, optional):
            Font uses for text.
            Defaults to pygame.font.SysFont("comiscans", 60).

            font_color (tuple[int, int, int], optional):
            Font color used for all font.
            Defaults to (65, 65, 65).

            title_text (list[tuple[str, tuple[int, int]]], optional):
            titles, in a list with title's text and the title coordinate.
            Defaults to [].

            button_font (pygame.font.Font, optional):
            Font uses for button.
            Defaults to pygame.font.SysFont("comiscans", 30).

            button_color (tuple[int, int, int], optional):
            Button color.
            Defaults to (161, 227, 168).

            buttons (list[tuple[str, tuple[int, int, int, int]]], optional):
            buttons, in a list with button text and button size (x, y, width, height)
            Defaults to [].
        """
        if isinstance(background, tuple):
            window.fill(background)
        else:
            window.blit(background, (0, 0))
        for title in title_text:
            text = title_font.render(title[0], 1, font_color)
            window.blit(text, title[1])
        for button in buttons:
            graphics.render_button(
                window, button[0], button[1], button_font, font_color, button_color
            )
        pygame.display.update()
