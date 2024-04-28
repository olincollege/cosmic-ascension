"""
This module contains the Controller class, intended to
take user inputs and apply certain actions accordingly.
It acts as the Controller section of MVC architecture.
"""

import pygame
from pygame.locals import *
import sys
import random

vector = pygame.math.Vector2


class Controller:
    """
    Dictates actions to be completed based on specified user inputs.

    Attributes:
        _jumping: A bool representing whether the character is jumping
            or not.
        _dead: A bool to indicate whether the character's status in the game,
            either alive or dead.
        _left_right: A float representing the horizontal acceleration of the
            character.
    """

    def __init__(self) -> None:
        """
        Initializes the default actions to be applied to the character.

        Args:
            none
        """
        self._jumping = False
        self._dead = False
        self._left_right = 0.0

    def update(self):
        """
        Updates the actions on the player based on key events.

        Args:
            none
        """
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
                if event.key == pygame.K_LEFT and self._left_right == -0.5:
                    self._left_right = 0.0
                if event.key == pygame.K_RIGHT and self._left_right == 0.5:
                    self._left_right = 0.0
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

    @property
    def left_right(self):
        """
        Returns the horizontal movement as a private attribute
        Args:
            none
        Returns:
            The horizontal acceleration of the character as a float
        """
        return self._left_right
