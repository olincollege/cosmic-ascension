"""
This module creates a class to generate a view for a user based on the model.
It acts as the View section of MVC architecture.

Note: This file cannot be tested as it controls display and visuals.
"""

import pygame


pygame.font.init()
pygame.mixer.init()
FONT = pygame.font.Font("Font/PressStart2P-Regular.ttf", 15)


class View:
    """
    Creates the view of the game for the player.
    """

    def __init__(self, model) -> None:
        """
        Initializes attributes that will be used to
        display the model

        Args:
            model: An instance of the Model class

        Attributes:
            _model: An instance of Model class
            _background_sound: pygame.mixer.Sound() that
                is the background music of the game
            _end_sound: pygame.mixer.Sound() that is the
                end screen sound effect played
            _easy_button: An instance of the Button class
                that represents the button on the menu screen
                that is used to select easy mode
            _medium_button: An instance of the Button class
                that represents the button on the menu screen
                that is used to select medium mode
            _hard_button: An instance of the Button class
                that represents the button on the menu screen
                that is used to select hard mode
            _rocket_move_sprite: A pygame.Surface() that represents
                the rocket jumping sprite
        """
        self._model = model
        self._background_sound = pygame.mixer.Sound(
            "sounds/background_sound.mp3"
        )
        self._background_sound.play(loops=-1)
        self._end_sound = pygame.mixer.Sound("sounds/end_sound.wav")
        self._easy_button = Button((25, 200), "EASY")
        self._medium_button = Button((150, 200), "MEDIUM")
        self._hard_button = Button((275, 200), "HARD")
        self._rocket_move_sprite = pygame.image.load(
            "sprites/rocket_move_0.png"
        )
        self._rocket_move_sprite = pygame.transform.scale(
            self._rocket_move_sprite,
            (
                self._model.player.rect.width,
                self._model.player.rect.width
                * (
                    self._rocket_move_sprite.get_height()
                    / self._rocket_move_sprite.get_width()
                ),
            ),
        )

    def draw_menu(self, displaysurface):
        """
        Draws menu screen for the user to view

        Args:
            displaysurface: A pygame.display representing the window
                to view
        """
        displaysurface.fill((0, 0, 0))
        self._easy_button.display(displaysurface)
        self._medium_button.display(displaysurface)
        self._hard_button.display(displaysurface)

    def draw_game(self, displaysurface):
        """
        Draws game screen for the user to view

        Args:
            displaysurface: A pygame.display representing the window
                to view
        """
        displaysurface.fill((0, 0, 0))
        for platform in self._model.platforms:
            displaysurface.blit(platform.surf, platform.rect)
        if self._model.player.velocity.y < 0:
            displaysurface.blit(
                self._rocket_move_sprite, self._model.player.rect
            )
        else:
            displaysurface.blit(
                self._model.player.image, self._model.player.rect
            )

    def draw_timer(self, time, displaysurface):
        """
        Draws the timer onto the display

        Args:
            displaysurface: A pygame.display representing the window
                to view
        """
        timer_text = FONT.render(time, True, (255, 255, 255))
        displaysurface.blit(timer_text, timer_text.get_rect(center=(200, 50)))

    def draw_score(self, displaysurface):
        """
        Draws the score onto the display

        Args:
            displaysurface: A pygame.display representing the window
                to view
        """
        score_text = FONT.render(
            f"SCORE: {self._model.score}", True, (255, 255, 255)
        )
        displaysurface.blit(score_text, (10, 10))

    def draw_game_over(self, displaysurface):
        """
        Draws game over for the user to view

        Args:
            displaysurface: A pygame.display representing the window
                to view
        """
        displaysurface.fill((0, 0, 0))
        game_over = FONT.render("GAME OVER", True, (255, 255, 255))
        score_text = FONT.render(
            f"SCORE: {self._model.score}", True, (255, 255, 255)
        )
        displaysurface.blit(game_over, game_over.get_rect(center=(200, 150)))
        displaysurface.blit(score_text, score_text.get_rect(center=(200, 200)))
        self._background_sound.stop()
        self._end_sound.play()

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


class Button:
    """
    Creates a the view for a button in the game
    """

    def __init__(self, topleft, text) -> None:
        """
        Initializes attributes that will be used to
        display the button

        Attributes:
            _topleft: A tuple representing the topleft
                coordinate of the button
            _text: A string representing the text to be displayed
                on the button
            _text_color: A tuple representing the RGB value of the
                color the text of the button will be. This value
                will be set to (0, 0, 0)
            _width: An int representing the width of the button.
                This value will be set to 100
            _height: An int representing the height of the button
                This value will be set to 50
            _button_color: A tuple representing the RGB value of the
                color of the button. This value will be set to
                (210, 210, 210)
            _button_surf: A pygame.Surface() that represents the surface
                of the button
            _button_rect: A pygame.Rect() that represents the hitbox of
                the button
            _text_surf: A pygame.Surface() that represents the surface
                of the button text
            _text_rect: A pygame.Rect() that represents the position of
                the text of the button
        """
        self._topleft = topleft
        self._text = text
        self._text_color = (0, 0, 0)
        self._width = 100
        self._height = 50
        self._button_color = (210, 210, 210)
        self._button_surf = pygame.Surface((self._width, self._height))
        self._button_surf.fill(self._button_color)
        self._button_rect = self._button_surf.get_rect(topleft=self._topleft)
        self._text_surf = FONT.render(self._text, True, self._text_color)
        self._text_rect = self._text_surf.get_rect(
            center=self._button_rect.center
        )

    def display(self, displaysurface):
        """
        Draws a buttons for the user to view

        Args:
            displaysurface: A pygame.display representing the window
                to view.
        """
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
