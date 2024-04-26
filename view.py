"""
This module creates a class to generate a view for a user based on the model. 
It acts as the View section of MVC architecture.
"""

import pygame
from pygame.locals import *
import sys
import random


vector = pygame.math.Vector2


class View:
    """
    Creates the view of the game for the player.

    Attributes:
        _model: An private attribute of an instance of the model to be viewed.
    """

    def __init__(self, model) -> None:
        """
        Initializes the model to be viewed.

        Args:
            model: An instance of the Model class.
        """
        self._model = model

    def draw(self, displaysurface):
        """
        Draws a display for the user to view/

        Args:
            displaysurface: A surface object representing the window
                to view.
        """
        displaysurface.fill((0, 0, 0))
        displaysurface.blit(self._model.player.surf, self._model.player.rect)
        for platform in self._model.platforms:
            displaysurface.blit(platform.surf, platform.rect)
