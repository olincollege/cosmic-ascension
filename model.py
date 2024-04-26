import pygame
from pygame.locals import *
import sys
import random


vector = pygame.math.Vector2

class Model():
    def __init__(self, platforms) -> None:
        self._gravity = vector(0, 0.5)
        self._friction = 0.12
        self._player = Player(self._gravity, self._friction)
        self._platforms = platforms
    def update(self, x_acceleration, jumping):
        self._player.move(x_acceleration)
        hits = pygame.sprite.spritecollide(self._player, self._platforms, False)
        if hits and not jumping:
            if self._player.rect.bottom < hits[0].rect.bottom:
                self._player.set_velocity(vector(self._player.velocity.x, 0))
                self._player.set_position(vector(self._player.position.x, hits[0].rect.top - 29))
        if jumping and hits:
            self._player.set_velocity(vector(self._player.velocity.x, -15))
        self._player.update()

    def platform_generation(self):
        while len(self._platforms) < 2:
            latest_platform = len(self._platforms)
            previous_platform = self._platforms.sprites()[latest_platform-1]
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
    def __init__(self, surf=None, color = (0,255,0), topleft=None) -> None:
        super().__init__()
        if surf is None:
            self._surf = pygame.Surface((random.randint(50,100), 7))
        else:
            self._surf = surf
        self._surf.fill(color)
        if topleft is None:
            topleft = (random.randint(0,450),random.randint(0, 400))
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
    def __init__(self, gravity, friction) -> None:
        super().__init__()
        self._gravity = gravity
        self._friction = friction
        self._acceleration = vector(0,0)
        self._velocity = vector(0,0)
        self._position = vector(10, 310)
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255,255,0))
        self._rect = self._surf.get_rect(topleft=self._position)

    def update(self):
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255,255,0))
        self._rect = self._surf.get_rect(topleft=self._position)
    def set_position(self, position):
        self._position = position

    def set_velocity(self, velocity):
        self._velocity = velocity

    def move(self, x_acceleration):
        print(self._velocity)
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
