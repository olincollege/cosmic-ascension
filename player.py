"""
This module contains a class to control the sprite based
upon the players specified inputs.    
"""

from math import copysign
from pygame.math import Vector2
from pygame.locals import KEYDOWN, KEYUP, K_LEFT, K_RIGHT
from pygame.sprite import collide_rect
from pygame.event import Event

from singleton import Singleton
from sprite import Sprite
from levels import Level
import game_settings as config


class Player(Sprite, Singleton):
    """
    A class to edit the sprite based on player inputs

    Args:
        Sprite: An instance of the sprite class
        Singleton: An instance of the singelton class
    """
