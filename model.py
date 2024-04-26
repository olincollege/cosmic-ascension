"""
This module creates a class to interact with data and the controller of
user inputs. It acts as the Model section of MVC architecture.
"""

import pygame
from pygame.locals import *
import sys
import random
import math
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
        self._controller = controller

    def update(self, x_acceleration, jumping):
        """
        Updates the character based on a given horizontal acceleration
        and jumps acting on it.

        Args:
            x_acceleration: An int representing how fast the character accelerates
            in a horizontal direction.
        """
        self._player.move(x_acceleration)
        hits = pygame.sprite.spritecollide(self._player, self._platforms, False)
        if hits and jumping:
            self._player.set_velocity(vector(self._player.velocity.x, -15))
        else:
            jumping = False
        # print(hits)
        if self._player.velocity.y > 0:
            if hits:
                # print(self._player.rect.bottom)
                # print(hits[0].rect.bottom)
                if self._player.position.y < hits[0].rect.bottom:
                    self._player.set_velocity(vector(self._player.velocity.x, 0))
                    self._player.set_position(
                        vector(self._player.position.x, hits[0].rect.top - 29)
                    )
                    jumping = False
        self._player.update()

    def platform_generation(self):
        while len(self._platforms) < 10:
            latest_platform = len(self._platforms) - 1
            previous_platform = self._platforms.sprites()[latest_platform]
            left = previous_platform.rect.left
            right = previous_platform.rect.right
            center = previous_platform.rect.center
            # print(left)
            # print(right)
            velocity_x_max = math.sqrt(2 * 0.5 * (right - left))
            # print(velocity_x_max)
            max_y_height = (15**2) / (2 * self._gravity.y)
            # print(max_y_height)
            fall_time = math.sqrt(2 * max_y_height / self._gravity.y)
            # print(fall_time)
            max_x_distance = int(velocity_x_max * fall_time)
            # print(max_x_distance)
            surf = pygame.Surface((random.randint(50, 100), 12))
            width = surf.get_width()
            max_left_center = -max_x_distance + left + width/2
            max_right_center = max_x_distance + right - width/2
            if max_left_center < 0:
                max_left_center = width/2 + 10
            if max_right_center > 400:
                max_right_center = 400 - width/2 - 10
            center_platform_x = random.randint(int(max_left_center), int(max_right_center))
            x_distance = abs(center_platform_x - center[0])
            max_y_reach = (-15 / velocity_x_max) * x_distance + (self._gravity.y * x_distance ** 2) / (2 * velocity_x_max ** 2)
            max_y_reach_point = center[1] + int(max_y_reach)
            reach = random.randint(max_y_reach_point, center[1])
            center_platform_y = reach
            center_platform = (center_platform_x, center_platform_y)
            # print(center_platform)
            platform = Platform(surf=surf, center=center_platform)
            if pygame.sprite.spritecollideany(platform,self._platforms):
                continue
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

    def __init__(self, surf=None, color=(0, 255, 0), center=None) -> None:
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
        if center is None:
            center = (random.randint(0, 400), random.randint(0, 450))
        else:
            center = center
        self._rect = self._surf.get_rect(center=center)
    def set_rect(self, x, y):
        """
        Sets the rect of the platform.

        Args:
            position: A tuple representing the x and y location
                of the platform sprite.
        """
        self._rect.x = x
        self._rect.y = y
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
        self._position = vector(200, 310)
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
