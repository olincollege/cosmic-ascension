"""
This module creates instances of classes in order to create
a full occurance of the game.

Note: This file cannot be tested as it mainly calls other functions
and edits the visual display.
"""

import pygame
from view import View
from model import Model
from model import Platform
from controller import Controller

WIDTH = 400
HEIGHT = 450


class Game:
    """
    Creates a full iteration of the game, including scrolling.

    Attributes:
        _clock: A pygame Clock object representing how long the game
            has been running.
        _fps: An int representing the frames per second
        _timer: An int representing the time limit for the game.
        _screen: A pygame display representing the game window.
        _controller: An instance of the controller class.
        _model: An instance of the model class.
        _view: An instance of the view class.
        _controller: An instance of the controller class.
    """

    def __init__(self) -> None:
        """
        Initializes game attributes.

        Args:
            none
        """
        self._clock = pygame.time.Clock()
        self._fps = 60
        self._timer = 60 * self._fps
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        ground = Platform(surf=pygame.Surface((200, 20)), center=(200, 445))
        platforms = pygame.sprite.Group()
        platforms.add(ground)
        self._model = Model(platforms, WIDTH, HEIGHT)
        self._view = View(self._model)
        self._controller = Controller(self._view)

    def camera(self):
        """
        Controls the scrolling to follow the sprite's progression

        Args:
            none

        Returns:
            A bool representing if the camera needs to move or not
        """
        if self._model.player.rect.top <= HEIGHT / 3:
            new_position_y = self._model.player.position.y + abs(
                self._model.player.velocity.y
            )
            self._model.player.set_position(
                (self._model.player.position.x, new_position_y)
            )
            for plat in self._model.platforms:
                plat.set_rect(
                    plat.rect.x,
                    plat.rect.y + abs(self._model.player.velocity.y),
                )
                if plat.rect.top >= HEIGHT:
                    plat.kill()
            return True
        return False

    def start(self):
        """
        Dictates the start of game play.

        Args:
            none
        """
        # Handles the start menu
        difficulty = 0
        while difficulty == 0:
            difficulty = self._controller.update_menu()
            self._view.draw_menu(self._screen)
            pygame.display.update()

        # Handles game screen
        self._model.set_difficulty(difficulty)
        current_time = 0
        can_increase_score = True
        while not self._model.game_over and self._timer > 0:
            if self.camera() and self._model.player.velocity.y < 0:
                if can_increase_score:
                    self._model.increase_score()
                current_time = self._timer
                can_increase_score = False
            if current_time - self._timer > 1:
                can_increase_score = True

            self._model.platform_generation()
            self._view.draw_game(self._screen)
            self._view.draw_score(self._screen)
            self._controller.update_game()
            self._model.update(
                self._controller.left_right, self._controller.jumping
            )
            self._model.check_player_off_screen()
            self._clock.tick(self._fps)
            self._timer -= 1
            time = format(self._timer / self._fps, ".2f")
            self._view.draw_timer(time, self._screen)
            pygame.display.update()

        # Handles end screen
        self._view.draw_game_over(self._screen)
        while True:
            self._controller.update_game_over()
            pygame.display.update()
