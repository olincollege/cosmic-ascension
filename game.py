"""
This module creates instances of classes in order to create
a full occurance of the game.
"""

import pygame
from view import View
from model import Model
from model import Platform
from controller import Controller

WIDTH = 400
HEIGHT = 450


class Game:
    """
    Creates a full iteration of the game, including scrolling.

    Attributes:
        _clock: A pygame Clock object representing how long the game
            has been running.
        _fps: An int representing the frames per second
        _screen: A pygame display representing the game window.
        _controller: An instance of the controller class.
        _model: An instance of the model class.
        _view: An instance of the view class.
    """

    def __init__(self) -> None:
        """
        Initializes game attributes.

        Args:
            none
        """
        self._clock = pygame.time.Clock()
        self._fps = 60
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        ground = Platform(surf=pygame.Surface((200, 20)), center=(200, 445))
        platforms = pygame.sprite.Group()
        platforms.add(ground)
        self._model = Model(platforms, WIDTH, HEIGHT)
        self._view = View(self._model)
        self._controller = Controller(self._view)

    def camera(self):
        """
        Controls the scrolling to follow the sprite's progression

        Args:
            none
        """
        if self._model.player.rect.top <= HEIGHT / 3:
            new_position_y = self._model.player.position.y + abs(
                self._model.player.velocity.y
            )
            self._model.player.set_position(
                (self._model.player.position.x, new_position_y)
            )
            for plat in self._model.platforms:
                plat.set_rect(
                    plat.rect.x, plat.rect.y + abs(self._model.player.velocity.y)
                )
                if plat.rect.top >= HEIGHT:
                    plat.kill()
            return True
        return False

    def start(self):
        """
        Dictates the start of game play.

        Args:
            none
        """
        difficulty = 0
        while difficulty == 0:
            difficulty = self._controller.update_menu()
            self._view.draw_menu(self._screen)
            pygame.display.update()
        self._model.set_difficulty(difficulty)
        while True:
            if self.camera() and self._model.player.velocity.y < 0:
                self._model.increase_score()
            self._model.platform_generation()
            self._view.draw_game(self._screen)
            self._view.draw_score(self._screen)
            self._controller.update_game()
            self._model.update(self._controller.left_right, self._controller.jumping)
            pygame.display.update()
            self._clock.tick(self._fps)
