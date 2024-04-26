import pygame
from pygame.locals import *
import sys
import random



vector = pygame.math.Vector2

class View():
    def __init__(self, model) -> None:
        self._model = model
    def draw(self, displaysurface):
        displaysurface.fill((0,0,0))
        displaysurface.blit(self._model.player.surf, self._model.player.rect)
        for platform in self._model.platforms:
            displaysurface.blit(platform.surf, platform.rect)



