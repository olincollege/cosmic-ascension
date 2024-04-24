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
    def __init__(self, surf=pygame.Surface((random.randint(50,100), 5)), color = (0,255,0), topleft=None) -> None:
        super().__init__()
        if surf is None:
            self._surf = pygame.Surface((random.randint(50,100), 5))
        else:
            self._surf = surf
        self._surf.fill(color)
        if topleft is None:
            topleft = (random.randint(0,450),random.randint(0, 400))
        else:
            topleft = topleft
        self._rect = self._surf.get_rect(topleft=topleft)
    @property
    def rect(self):
        return self._rect

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._position = vector(10, 310)
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255,255,0))
        self._rect = self._surf.get_rect(topleft=self._position)
    def update(self):
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255,255,0))
        self._rect = self._surf.get_rect(topleft=self._position)
    @property
    def position(self):
        return self._position
    @property
    def rect(self):
        return self._rect
