import pygame
from pygame.locals import *
import sys
import random

vector = pygame.math.Vector2

class Controller():
    def __init__(self) -> None:
        self._jumping = False
        self._dead = False
        self._left_right = 0
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._left_right = -0.5
                if event.key == pygame.K_RIGHT:
                    self._left_right = 0.5
                if event.key == pygame.K_SPACE:
                    self._jumping = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self._jumping = False
                if event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                    self._left_right = 0
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    