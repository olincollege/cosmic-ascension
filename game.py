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

class Game():
    def __init__(self) -> None:
        self._clock = pygame.time.Clock()
        self._fps = 60
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        ground = Platform(surf=pygame.Surface((WIDTH, 20)), color=(255,0,0), topleft=(0, HEIGHT - 10))
        platforms = pygame.sprite.Group()
        platforms.add(ground)
        self._model = Model(platforms)
        self._controller = Controller()
        self._view = View(self._model)
    def start(self):
        while True:
            self._screen.blit(self._model.player.surf, self._model.player.rect)
            self._view.draw(self._screen)
            self._controller.update()
            self._model.update(self._controller._left_right, self._controller._jumping)
            pygame.display.update()
            self._clock.tick(self._fps)