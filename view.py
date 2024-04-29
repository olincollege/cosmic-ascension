"""
This module creates a class to generate a view for a user based on the model. 
It acts as the View section of MVC architecture.
"""

import pygame
from pygame.locals import *


vector = pygame.math.Vector2
pygame.font.init()
font = pygame.font.Font(None, 36)

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
        self._easy_button = Button((25, 200), "Easy")
        self._medium_button = Button((150, 200), "Medium")
        self._hard_button = Button((275, 200), "Hard")

    def draw_menu(self, displaysurface):
        displaysurface.fill((0, 0, 0))
        self._easy_button.display(displaysurface)
        self._medium_button.display(displaysurface)
        self._hard_button.display(displaysurface)
        
    def draw_game(self, displaysurface):
        """
        Draws a display for the user to view

        Args:
            displaysurface: A surface object representing the window
                to view.
        """
        displaysurface.fill((0, 0, 0))
        displaysurface.blit(self._model.player._image, self._model.player.rect)
        for platform in self._model.platforms:
            displaysurface.blit(platform.surf, platform.rect)
    def draw_timer(self, time, displaysurface):
        timer_text = font.render(time, True, (255, 255, 255))
        displaysurface.blit(timer_text, timer_text.get_rect(center = (200,50)))
        
    def draw_score(self, displaysurface):
        """
        Draws the score onto the display

        Args:
            displaysurface: A surface object representing the window
                to view.
        """
        score_text = font.render(f"Score: {self._model.score}", True, (255, 255, 255))
        displaysurface.blit(score_text, (10, 10))

    def draw_game_over(self, displaysurface):
        displaysurface.fill((0, 0, 0))
        game_over = font.render("GAME OVER", True, (255, 255, 255))
        score_text = font.render(f"SCORE: {self._model.score}", True, (255, 255, 255))
        displaysurface.blit(game_over, game_over.get_rect(center=(200, 150)))
        displaysurface.blit(score_text, score_text.get_rect(center=(200, 200)))

    @property
    def easy_button(self):
        """
        Allows the private attribute _easy_button to be output

        Returns:
            Private attribute _easy_button which is a Button object
        """
        return self._easy_button
    
    @property
    def medium_button(self):
        """
        Allows the private attribute _medium_button to be output

        Returns:
            Private attribute _medium_button which is a Button object
        """
        return self._medium_button
    
    @property
    def hard_button(self):
        """
        Allows the private attribute _hard_button to be output

        Returns:
            Private attribute _hard_button which is a Button object
        """
        return self._hard_button
    


class Button():
    def __init__(self, topleft, text, text_color=(0, 0, 0), button_color=(210,210,210), width=100, height=50) -> None:
        self._topleft = topleft
        self._text = text
        self._text_color = text_color
        self._width = width
        self._height = height
        self._button_color = button_color
        self._button_surf = pygame.Surface((self._width, self._height))
        self._button_surf.fill(self._button_color)
        self._button_rect = self._button_surf.get_rect(topleft=self._topleft)
        self._text_surf = font.render(self._text, True, self._text_color)
        self._text_rect = self._text_surf.get_rect(center=self._button_rect.center)

    def display(self, displaysurface):
        displaysurface.blit(self._button_surf, self._button_rect)
        displaysurface.blit(self._text_surf, self._text_rect)
    
    @property
    def button_rect(self):
        """
        Allows private attribute _button_rect to be output

        Return:
            Private attribute _button_rect which is of pygame.Rect()
        """
        return self._button_rect