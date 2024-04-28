"""
This module creates a class to interact with data and the controller of
user inputs. It acts as the Model section of MVC architecture.
"""

import pygame
from pygame.locals import *
import random
import math


vector = pygame.math.Vector2


class Model:
    """
    Class that acts as Model part of MVC architecture.
    Updates the data related to the game play.

    Attributes:
        _gravity: pygame.math.Vector2 that represents
            the gravity in the game
        _friction: An float representing the friction
             associated
            with the characters interactions with
                objects in game.
        _player: An instance of the Player class
            representing the player character
        _platform_num: An int representing the max
            number of platforms generated at any given time
        _platforms: pygame.sprite.Group() of platforms
            in the game
        _game_difficulty: An int representing the difficulty
            of the game. 1 is the max difficulty, 0.5 is the
            game's easy mode, and 0.75 is the game's medium
        _score: int representing the score of the game
        _screen_width: int representing the width of the
            display screen
        _screen_height: int representing the height of the
            display screen
    """

    def __init__(self, platforms, width, height) -> None:
        """
        Initializes the model.

        Args:
            platforms: pygame.sprite.Group() representing the
                current platforms in the game
            width: int representing the width of the display
                screen
            height: int representing the height of the display
                screen    Attributes:
        _gravity: pygame.math.Vector2 that represents
            the gravity in the game
        _friction: An float representing the friction
             associated
            with the characters interactions with
                objects in game.
        _player: An instance of the Player class
            representing the player character
        _platform_num: An int representing the max
            number of platforms generated at any given time
        _platforms: pygame.sprite.Group() of platforms
            in the game
        _game_difficulty: An int representing the difficulty
            of the game. 1 is the max difficulty, 0.5 is the
            game's easy mode, and 0.75 is the game's medium
        _score: int representing the score of the game
        _screen_width: int representing the width of the
            display screen
        _screen_height: int representing the height of the
            display screen
        """
        self._gravity = vector(0, 0.35)
        self._friction = 0.12
        self._player = Player(self._gravity, self._friction)
        self._platform_num = 30
        self._platforms = platforms
        self._game_difficulty = 1
        self._score = 0
        self._screen_width = width
        self._screen_height = height

    def update(self, x_acceleration, jumping):
        """
        Updates the character based on a given horizontal acceleration
        and jumps acting on it.

        Args:
            x_acceleration: A float representing how fast the character accelerates
            in a horizontal direction.
            jumping: A bool representing if the character is jumping or not.
        """
        # Set the player x acceleration and move character based on it
        self._player.move(x_acceleration)

        # Check if the player is touching any platform
        hits = pygame.sprite.spritecollide(self._player, self._platforms, False)

        # If player is not moving upwards and touching a platform
        if self._player.velocity.y >= 0 and hits:
            # If botto of player is above the bottom of the platform
            if (self._player.rect.bottom) < hits[0].rect.bottom:
                # Then set the velocity y velocity of the player to 0 
                # and put its position to on top of the platform
                self._player.set_velocity(vector(self._player.velocity.x, 0))
                self._player.set_position(
                    vector(
                        self._player.position.x,
                        hits[0].rect.top - self._player.rect.height / 2,
                    )
                )
                # If the player is holding down the space bar, override the previous
                # y velocity setting and change it to jump velocity 
                if jumping:
                    self._player.set_velocity(
                        vector(self._player.velocity.x, self._player.jump_velocity)
                    )
        # Update the player's rect
        self._player.update()

    def platform_generation(self):
        """
        Controls generation of platforms during game play

        Args:
            none

        Note:
            The calculation for the platform distances are based off
            physics kinematics equations.
        """
        while len(self._platforms) < self._platform_num:
            # Get previous platform dimensions
            latest_platform = len(self._platforms) - 1
            previous_platform = self._platforms.sprites()[latest_platform]
            left = previous_platform.rect.left
            right = previous_platform.rect.right
            center = previous_platform.rect.center

            # Calculate the maximum x velocity the player can reach based
            # on how long the previous platform is
            velocity_x_max = math.sqrt(2 * 0.5 * (right - left))

            # Calculate maximum height player can reach
            max_y_height = self._game_difficulty * (
                ((-self._player.jump_velocity) ** 2) / (2 * self._gravity.y)
            )

            # Calculate how long it takes to fall from this height
            fall_time = math.sqrt(2 * max_y_height / self._gravity.y)

            # Calculate how far player can move in that time
            max_x_distance = int(velocity_x_max * fall_time)

            # Generate new platform dimensions
            surf = pygame.Surface((random.randint(50, 100), 15))
            new_platform_width = surf.get_width()
            new_platform_height = surf.get_height()

            # Accounting for take off and landing of player. Gives more leeway at higher difficult to
            # account for reaction time. Can't expect player to make perfect jump to maximize height
            # and distance every time
            player_width = self._player.rect.width
            max_x_distance -= player_width * 3.5 * self._game_difficulty

            # Accounting for difficulty level
            max_x_distance = max_x_distance * self._game_difficulty

            # Calculate maximum reachable range
            max_left = left - max_x_distance
            max_right = right + max_x_distance

            # Calculating range where player can reach max height
            total_range = max_right - max_left
            left_reach_max = max_left + total_range / 4
            right_reach_max = max_right - total_range / 4

            # Calculating range of x that player can reach and are still on screen
            if max_left < 0:
                max_left = 0
            if max_right > self._screen_width:
                max_right = self._screen_width

            # Account for difficulty
            max_left = int(max_left)
            max_right = int(max_right)
            full_range = max_right - max_left
            minimum_left_x = (
                int(max_left + (full_range / 2) * (1 - self._game_difficulty)) + 1
            )
            minimum_right_x = (
                int(max_right - (full_range / 2) * (1 - self._game_difficulty)) - 1
            )

            # Calculate landing x value
            x_landing = random.choice(
                [
                    i
                    for i in range(max_left, max_right)
                    if i not in range(minimum_left_x, minimum_right_x)
                ]
            )
            # Check if player needs to jump left or right of current platform
            if x_landing < center[0]:
                is_left = True
            else:
                is_left = False

            # Calculate center of new platform
            if x_landing < new_platform_width / 2:
                new_platform_center_x = new_platform_width / 2
            elif x_landing > (self._screen_width - new_platform_width / 2):
                new_platform_center_x = self._screen_width - new_platform_width / 2
            else:
                if is_left:
                    new_platform_center_x = (
                        x_landing - new_platform_width / 2 + player_width / 2
                    )
                else:
                    new_platform_center_x = (
                        x_landing + new_platform_width / 2 - player_width / 2
                    )

            # Check if landing is in range of where max height is reachable. If not, calculate max reachable y
            if x_landing > left_reach_max or x_landing < right_reach_max:
                max_y_reach = max_y_height
            else:
                if x_landing < left_reach_max:
                    x_distance = left_reach_max - x_landing
                else:
                    x_distance = x_landing - right_reach_max
                time = x_distance / velocity_x_max
                max_y_reach = max_y_height - 0.5 * self._gravity.y * time**2
            max_y_reach = int(max_y_reach)
            max_y_reach_point = center[1] - max_y_reach

            # Adjust difficulty level
            minimum_y = center[1] - max_y_reach + 1

            new_platform_center_y = (
                random.randint(max_y_reach_point, minimum_y) + new_platform_height / 2
            )

            center_platform = (new_platform_center_x, new_platform_center_y)
            platform = Platform(surf=surf, center=center_platform)
            if pygame.sprite.spritecollideany(platform, self._platforms):
                continue
            self._platforms.add(platform)

    def increase_score(self):
        """
        Increases the private attribute _score by 1

        Args:
            None

        Return:
            None
        """
        self._score += 1

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

    @property
    def score(self):
        """
        Returns the score of the game
        Args:
            none
        Returns:
            The score attribute
        """
        return self._score


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
        self._jump_velocity = -10
        self._acceleration = vector(0, 0)
        self._velocity = vector(0, 0)
        self._position = vector(200, 310)
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255, 255, 0))
        self._rect = self._surf.get_rect(center=self._position)

    def update(self):
        """
        Updates the character surface, shape, and color.

        Args:
            none
        """
        self._surf = pygame.Surface((30, 30))
        self._surf.fill((255, 255, 0))
        self._rect = self._surf.get_rect(center=self._position)

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
    def jump_velocity(self):
        """
        Returns whether or not player is jumping

        Returns:
            boolean representing whether or not the player is jumping
        """
        return self._jump_velocity

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
