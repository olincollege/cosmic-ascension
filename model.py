import pygame
from pygame.locals import *
import sys
import random


vector = pygame.math.Vector2

class Model():
    def __init__(self, platforms) -> None:
        self._player = Player()
        self._platforms = platforms

class Platform(pygame.sprite.Sprite):
    def __init__(self, surf=pygame.Surface((random.randint(50,100), 12)), color = (0,255,0), topleft=(random.randint(0,450-10),
                                                 random.randint(0, 400-30))) -> None:
        super().__init__()
        self._surf = surf
        self._surf.fill(color)
        self.rect = self._surf.get_rect(topleft=topleft)

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._position = vector(10, 320)
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255,255,0))
        self.rect = self._surf.get_rect(topleft=self._position)
    def update(self):
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255,255,0))
        self.rect = self._surf.get_rect(topleft=self._position)
