import pygame
from pygame.locals import *
import sys
import random

vector = pygame.math.Vector2


class Controller:
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
                    print("jump")
                    self._jumping = True
                else:
                    self._jumping = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self._jumping = False
                if event.key == pygame.K_LEFT and self._left_right == -0.5:
                    self._left_right = 0
                if event.key == pygame.K_RIGHT and self._left_right == 0.5:
                    self._left_right = 0
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    @property
    def jumping(self):
        """
        Returns the jumping bool as a private attribute
        Args:
            none
        Returns:
            If the player is jumping or not
        """
        return self._jumping
