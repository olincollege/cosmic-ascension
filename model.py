import pygame
from pygame.locals import *
import sys
import random
import math


vector = pygame.math.Vector2


class Model:
    def __init__(self, platforms) -> None:
        self._gravity = vector(0, 0.5)
        self._friction = 0.12
        self._player = Player(self._gravity, self._friction)
        self._platforms = platforms

    def update(self, x_acceleration, jumping):
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
            print(velocity_x_max)
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
            print(center_platform)
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
    def __init__(self, surf=None, color=(0, 255, 0), center=None) -> None:
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
    def __init__(self, gravity, friction) -> None:
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
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255, 255, 0))
        self._rect = self._surf.get_rect(topleft=self._position)

    def set_position(self, position):
        self._position = position

    def set_velocity(self, velocity):
        self._velocity = velocity

    def move(self, x_acceleration):
        # print(self._velocity)
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
