import pygame
from pygame.locals import *
import sys
import random

vector = pygame.math.Vector2


class Controller(pygame.sprite.Sprite):
    def __init__(self, model) -> None:
        super().__init__()
        self._model = model
        self._velocity = vector(0, 0)
        self._acceleration = vector(0, 0)

    def move(self):
        self._acceleration = vector(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self._acceleration.x = -0.5
        if pressed_keys[K_RIGHT]:
            self._acceleration.x = 0.5
        self._acceleration.x += self._velocity.x * -0.12
        self._velocity.x += self._acceleration.x
        self._acceleration.y += self._velocity.y * -0.1
        self._velocity.y += self._acceleration.y
        self._model._player._position += self._velocity + 0.5 * self._acceleration
        self._model._player.update()
        if self._acceleration.x < 0.1 or self._acceleration.x > -0.1:
            self._acceleration.x = 0
        if self._velocity.y > 0:
            hits = pygame.sprite.spritecollide(
                self._model._player, self._model._platforms, False
            )
            if hits:
                if self._model._player._position.y + 30 < hits[0].rect.bottom:
                    self._velocity.y = 0
                    self._model._player._position.y = hits[0].rect.top - 30

    def jump(self):
        hits = pygame.sprite.spritecollide(
            self._model._player, self._model._platforms, False
        )
        if hits:
            self._velocity.y = -30
