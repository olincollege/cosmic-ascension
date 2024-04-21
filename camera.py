"""
Contains a class that updates the user’s view based on 
the character’s movements. Tracks the movement and 
location of the character.
    
Manage scrolling of the platform vertically

"""

from pygame import Rect
from sprite import Sprite

from singleton import Singleton
import game_settings as config


class Camera:
    """
    A class to represent the camera scrolling
    during gameplay.
    """

    def __init__(self, lerp=5, width=config.XWIN, height=config.YWIN):
        """
        Initializes the camera window view.

        Args:
            lerp: An int representing the mode to calculate scrolling speed.
                Defaults to 5.
            width: An int representing the width of the window.
                Defaults to config.XWIN, from game_settings
            height: An int representing the width of the window.
                Defaults to config.YWIN, from game_settings
        """

        self.state = Rect(0, 0, width, height)
        self.lerp = lerp
        self.center = height // 2
        self.maxheight = self.center

    def reset(self) -> None:
        """
        Resets the game window after the game ends.
        """
        self.state.y = 0
        self.maxheight = self.center
