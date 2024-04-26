"""
This module creates a class to interact with data and the controller of
user inputs. It acts as the Model section of MVC architecture.
"""

import pygame
from pygame.locals import *
import sys
import random
from controller import Controller


vector = pygame.math.Vector2


class Model:
    """
    Class that acts as Model part of MVC architecture.
    Updates the data related to the game play.

    Attributes:
        _gravity: A vector representing the acceleration associated
            with gravity that acts on the character.
        _friction: An int representing the value friction associated
            with the characters interactions with objects in game.
        _player: An instance of the Player class, with the gravity
            and friction attributes applied to it.
        _platforms: Platform instances that are present in the model.
    """

    def __init__(self, platforms, controller) -> None:
        """
        Initializes the model.

        Args:
            platforms: The intial Platform instances to start the game with.
            controller: An instance of the Controller class
        """
        self._gravity = vector(0, 0.5)
        self._friction = 0.12
        self._player = Player(self._gravity, self._friction)
        self._platforms = platforms
        self._controll = controller

    def update(self, x_acceleration, jumps=False):
        """
        Updates the character based on a given horizontal acceleration
        and jumps acting on it.

        Args:
            x_acceleration: An int representing how fast the character accelerates
            in a horizontal direction.
        """
        self._player.move(x_acceleration)
        hits = pygame.sprite.spritecollide(self._player, self._platforms, False)
        print(f"hits: {hits}")
        print(f"is jumping? {self._controll.jumping}")
        if hits != [] and self._controll.jumping is True:
            self._player.set_velocity(vector(self._player.velocity.x, -15))

        # print(f"hits: {hits}")
        if self._player.velocity.y > 0:
            if hits:
                # print(f"bottom of rect: {self._player.rect.bottom}")
                # print(f"hit top of plat: {hits[0].rect.top}")
                if self._player.position.y < hits[0].rect.top - 1:
                    self._player.set_velocity(vector(self._player.velocity.x, 0))
                    self._player.set_position(
                        vector(self._player.position.x, hits[0].rect.top - 29)
                    )
        self._player.update()

    def platform_generation(self):
        """
        Generates platforms based on the number of existing platforms in frame.

        Args:
            none
        """
        while len(self._platforms) < 6:
            latest_platform = len(self._platforms)
            previous_platform = self._platforms.sprites()[latest_platform - 1]
            left = previous_platform.rect.left
            right = previous_platform.rect.right
            top = previous_platform.rect.top
            bottom = previous_platform.rect.bottom

            platform = Platform()
            self._platforms.add(platform)

    @property
    def player(self):
        """
        Returns the player as a private attribute
        Args:
            none
        Returns:
            The player attribute of the model.
        """
        return self._player

    @property
    def platforms(self):
        """
        Returns the platforms objects as a private attribute
        Args:
            none
        Returns:
            The platforms attribute of the model.
        """
        return self._platforms


class Platform(pygame.sprite.Sprite):
    """
    Creates a platform for a sprite to interact with.

    Attributes:
        _surf: A pygame surface object that acts as a platform
            in gameplay.
        _rect: A rectangle object representing the area that
            the platform occupies.
    """

    def __init__(self, surf=None, color=(0, 255, 0), topleft=None) -> None:
        """
        Initializes the platforms.

        Args:
            surf: A surface representing platforms. Defaults to None.
            color: A tuple representing the platform RBG color code. Defaults to (0, 255, 0).
            topleft: A tuple representing the top left platform location. Defaults to None.
        """
        super().__init__()
        if surf is None:
            self._surf = pygame.Surface((random.randint(50, 100), 12))
        else:
            self._surf = surf
        self._surf.fill(color)
        if topleft is None:
            topleft = (random.randint(0, 450), random.randint(0, 400))
        else:
            topleft = topleft
        self._rect = self._surf.get_rect(topleft=topleft)

    @property
    def rect(self):
        """
        Returns the rectangle object as a private attribute
        Args:
            none
        Returns:
            The rectangle attribute of the model.
        """
        return self._rect

    @property
    def surf(self):
        """
        Returns the surface object as a private attribute
        Args:
            none
        Returns:
            The surface attribute of the model.
        """
        return self._surf


class Player(pygame.sprite.Sprite):
    """
    A class to generate and dictate actions of the game
    character sprite.

    Attributes:
        _gravity: A vector representing the acceleration associated
            with gravity that acts on the character.
        _friction: An int representing the value friction associated
            with the characters interactions with objects in game.
        _acceleration: A vector representing the acceleration
            acting on the character in any direction.
        _velocity: A vector representing the velocity of the character.
        _position: A vector representing the position of the character in
            the game window.
        _surf: A pygame surface object that acts as a platform
            in gameplay.
        _rect: A rectangle object representing the area that
            the platform occupies.
    """

    def __init__(self, gravity, friction) -> None:
        """
        Initializes the character.

        Args:
            gravity: A vector representing the acceleration
                on a character due to gravity.
            friction: An int representing the friction between character
                and platforms.
        """
        super().__init__()
        self._gravity = gravity
        self._friction = friction
        self._acceleration = vector(0, 0)
        self._velocity = vector(0, 0)
        self._position = vector(10, 310)
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255, 255, 0))
        self._rect = self._surf.get_rect(topleft=self._position)

    def update(self):
        """
        Updates the character surface, shape, and color.

        Args:
            none
        """
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255, 255, 0))
        self._rect = self._surf.get_rect(topleft=self._position)

    def set_position(self, position):
        """
        Sets the position of the player.

        Args:
            position: A tuple representing the x and y location
                of the character sprite.
        """
        self._position = position

    def set_velocity(self, velocity):
        """
        Sets the velocity of the player sprite.

        Args:
            velocity: A tuple representing the velocity
                in each direction for the sprite.
        """
        self._velocity = velocity

    def move(self, x_acceleration):
        """
        Dictates the horizontal motion of the player sprite.

        Args:
            x_acceleration: An int representing horizontal
                acceleration of the character.
        """
        self._acceleration = self._gravity
        self._acceleration.x = x_acceleration
        self._acceleration.x -= self._velocity.x * 0.12
        self._velocity.x += self._acceleration.x

        self._velocity.y += self._acceleration.y
        self._position += self._velocity + 0.5 * self._acceleration

        if self._acceleration.x < 0.1 or self._acceleration.x > -0.1:
            self._acceleration.x = 0

    @property
    def acceleration(self):
        """
        Returns the acceleration of player

        Returns:
            Acceleration of player in form of float
        """
        return self._acceleration

    @property
    def velocity(self):
        """
        Returns the velocity of player

        Returns
            Velocity of player in form of float
        """
        return self._velocity

    @property
    def position(self):
        """
        Returns the position as a private attribute
        Args:
            none
        Returns:
            The position attribute of the model.
        """
        return self._position

    @property
    def surf(self):
        """
        Returns the surface object as a private attribute
        Args:
            none
        Returns:
            The surface attribute of the model.
        """
        return self._surf

    @property
    def rect(self):
        """
        Returns the rectangle object as a private attribute
        Args:
            none
        Returns:
            The rectangle attribute of the model.
        """
        return self._rect
