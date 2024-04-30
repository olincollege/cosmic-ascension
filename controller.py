"""
This module contains the Controller class, intended to
take user inputs and apply certain actions accordingly.
It acts as the Controller section of MVC architecture.
"""

import sys
import pygame


class Controller:
    """
    Dictates actions to be completed based on specified user inputs.

    Attributes:
        _jumping: A bool representing whether the character is jumping
            or not.
        _left_right: A float representing the horizontal acceleration of the
            character.
    """

    def __init__(self, view) -> None:
        """
        Initializes attributes that store what the player is doing

        Args:
            none
        """
        self._view = view
        self._jumping = False
        self._left_right = 0.0

    def update_menu(self):
        """
        Updates what happens in menu based on player input

        Args:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if self._view.easy_button.button_rect.collidepoint(position):
                    return 0.5
                if self._view.medium_button.button_rect.collidepoint(position):
                    return 0.75
                if self._view.hard_button.button_rect.collidepoint(position):
                    return 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return 0

    def update_game(self):
        """
        Updates the actions of the player based player input

        Args:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._left_right = -0.5
                if event.key == pygame.K_RIGHT:
                    self._left_right = 0.5
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self._jumping = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self._left_right == -0.5:
                    self._left_right = 0.0
                if event.key == pygame.K_RIGHT and self._left_right == 0.5:
                    self._left_right = 0.0
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self._jumping = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_game_over(self):
        """
        Updates the what happens in game over screen

        Args:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    @property
    def jumping(self):
        """
        Returns the jumping bool as a private attribute
        Args:
            none
        Returns:
            If the player is jumping or not as boolean
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
