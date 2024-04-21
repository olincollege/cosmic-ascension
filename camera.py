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
    A class to represent the camera scrolling during gameplay.
    """

    def __init__(self, scroll_speed=5, width=config.XWIN, height=config.YWIN):
        """
        Initializes the camera window view.

        Args:
            scroll_speed: An int representing the mode to calculate scrolling speed.
                Defaults to 5.
            width: An int representing the width of the window.
                Defaults to config.XWIN, from game_settings
            height: An int representing the width of the window.
                Defaults to config.YWIN, from game_settings
        """

        self.state = Rect(0, 0, width, height)
        self.scroll_speed = scroll_speed
        self.center = height // 2
        self.max_height = self.center

    def reset_window(self):
        """
        Resets the game window after the game ends.

        Args:
            none
        """
        self.state.y = 0
        self.max_height = self.center

    def apply_window(self, rect: Rect):
        """
        Edits the rectangle window to match the camera position.

        Args:
            rect: The rectangle window to be transformed. pygame rectangle
            type.

        Returns:
            A rectangle type of the newly transformed camera window.
        """
        return rect.move((0, -self.state.topleft[1]))

    def apply(self, target: Sprite):
        """
        Gives a new position to target to render based on the current camera position.

        Args:
            target: A sprite instance seeking the correct render position.

        Returns:
            A retangle object of the new target render position.
        """
        return self.apply_window(target.rect)

    def update_window(self, target: Rect):
        """
        Scrolls the camera up to the highest height that the player
        has reached.

        Args:
            target: The target rectangle position to reach.
        """

        if target.y < self.max_height:
            self.max_height = target.y

        speed = ((self.state.y + self.center) - self.max_height) / self.scroll_speed
        self.state.y -= speed
