"""
This module creates instances of classes in order to create
a full occurance of the game.
"""

import pygame
from pygame.locals import *
import sys
import random
from view import View
from model import Model
from model import Platform
from controller import Controller

WIDTH = 400
HEIGHT = 450
# display = pygame.display.set_mode((WIDTH, HEIGHT))

# surf = pygame.Surface((30, 30))
# surf.fill((255,255,0))
# rect = surf.get_rect()
# class Game():
#     def start(self):
#         controller = Controller()
#         while True:
#             controller.update()
#             display.blit(surf, rect)
#             pygame.display.update()


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
        ground = Platform(
            surf=pygame.Surface((200, 20)), color=(255, 0, 0), center=(200, 445)
        )
        platforms = pygame.sprite.Group()
        platforms.add(ground)
        self._controller = Controller()
        self._model = Model(platforms, self._controller)
        self._view = View(self._model)

    def camera(self):
        """
        Controls the scrolling to follow the sprite's progression

        Args:
            none
        """
        if self._model.player.rect.top <= HEIGHT / 3:
            self._model.player.position.y += abs(self._model.player.velocity.y)
            for plat in self._model.platforms:
                plat.rect.y += abs(self._model.player.velocity.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

    def start(self):
        """
        Dictates the start of game play.

        Args:
            none
        """
        while True:
            self.camera()
            self._model.platform_generation()
            self._view.draw(self._screen)
            self._controller.update()
            self._model.update(self._controller._left_right, self._controller._jumping)
            pygame.display.update()
            self._clock.tick(self._fps)
