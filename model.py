"""
This module creates a class to interact with data and the controller of
user inputs. It acts as the Model section of MVC architecture.
"""

import random
import math
import pygame


VECTOR = pygame.math.Vector2


class Model:
    """
    Class that acts as Model part of MVC architecture.
    Updates the data related to the game play.

    Attributes:
            _gravity: pygame.math.Vector2 that represents
                the gravity in the game
            _friction: A float representing the friction
                associated with the characters interactions with
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
            _game_over: a boolean representing if player is on game over screen
            _jump_sound: wav file for the sound of the rockets when character
                jumps
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
                screen
        """
        self._gravity = VECTOR(0, 0.35)
        self._friction = 0.12
        self._player = Player(self._gravity, self._friction)
        self._platform_num = 30
        self._platforms = platforms
        self._game_difficulty = 0.5
        self._score = 0
        self._screen_width = width
        self._screen_height = height
        self._game_over = False
        self._jump_sound = pygame.mixer.Sound("sounds/rocketbrrrnoises.wav")

    def update(self, x_acceleration, jumping):
        """
        Updates the character based on a given horizontal acceleration
        and jumps acting on it.

        Args:
            x_acceleration: A float representing how fast the character
                accelerates in a horizontal direction.
            jumping: A bool representing if the character is jumping
                or not.
        """
        # Set the player x acceleration and move character based on it
        self._player.move(x_acceleration)

        # Check if the player is touching any platform
        hits = pygame.sprite.spritecollide(self._player, self._platforms, False)

        # If player is not moving upwards and touching a platform
        if self._player.velocity.y >= 0 and hits:
            # If bottom of player is above the bottom of the platform
            if (self._player.rect.bottom) < hits[0].rect.bottom:
                # Then set the velocity y velocity of the player to 0
                # and put its y position to on top of the platform
                self._player.set_velocity(VECTOR(self._player.velocity.x, 0))
                self._player.set_position(
                    VECTOR(
                        self._player.position.x,
                        hits[0].rect.top - self._player.rect.height / 2,
                    )
                )
                # If the player is holding down the space bar, override the
                # previous y velocity setting and change it to jump velocity
                if jumping:
                    self._player.set_velocity(
                        VECTOR(
                            self._player.velocity.x, self._player.jump_velocity
                        )
                    )
                    self._jump_sound.play()
        # Update the player's rect
        self._player.update()

    def check_player_off_screen(self):
        """
        Checks if the player is off screen. If so,
        switches game to game over

        Args:
            none
        """
        if (
            self._player.position.x < 0
            or self._player.position.x > self._screen_width
        ):
            self._game_over = True
        if self._player.position.y > self._screen_height:
            self._game_over = True

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

            # Accounting for difficulty level
            max_x_distance = max_x_distance * self._game_difficulty

            # Accounting for take off and landing of player. Gives
            # more leeway at higher difficult to account for reaction
            # time. Can't expect player to make perfect jump to
            # maximize height and distance every time
            max_x_distance -= (
                self._player.rect.width * 1.5 * self._game_difficulty
            )

            # Generate new platform dimensions
            surf = pygame.Surface((random.randint(50, 100), 15))
            new_platform_width = surf.get_width()
            new_platform_height = surf.get_height()

            # Calculate maximum reachable range
            max_left = int(left - max_x_distance)
            max_right = int(right + max_x_distance)

            # Calculating range where player can reach max height
            left_reach_max, right_reach_max = (
                self.calculate_range_player_reach_max_height(
                    max_left, max_right
                )
            )

            # Calculating range of x that player can reach and are still on
            # screen
            if max_left < 0:
                max_left = 0
            if max_right > self._screen_width:
                max_right = self._screen_width

            # Calculate landing x value
            x_landing = self.calculate_x_landing(max_left, max_right)

            # Calculate x of center of new platform
            new_platform_center_x = self.calculate_platform_center_x(
                x_landing, new_platform_width, center
            )

            # Calculate y of center of new platform
            new_platform_center_y = self.calculate_platform_center_y(
                (left_reach_max, right_reach_max),
                x_landing,
                max_y_height,
                center,
                velocity_x_max,
                new_platform_height,
            )

            # Calculate center of new platform
            center_platform = (new_platform_center_x, new_platform_center_y)
            platform = Platform(surf, center_platform)
            self._platforms.add(platform)

    def calculate_range_player_reach_max_height(self, max_left, max_right):
        """
        Calculates range in which the player can reach the maximum height

        Args:
            max_left: int that represents the maximum left x point that can be
                reached
            max_right: int that represents the maximum right x point that can
                be reached

        Return:
            left_reach_max and right_reach_max which are both floats that
            represent the point bounds in which the player can jump to its
            maximum height

        Note: This is based on projectile motion
        """
        # Calculating range where player can reach max height
        total_range = max_right - max_left
        left_reach_max = max_left + total_range / 4
        right_reach_max = max_right - total_range / 4
        return left_reach_max, right_reach_max

    def calculate_x_landing(self, max_left, max_right):
        """
        Calculates the x point that the player can land on.
        This is not the same as the furtherest point the
        player can reach. It is simply a random point that
        the player can reach and the game is using to generate
        a platform.

        Args:
            max_left: int that represents the maximum left x point that can be
                reached
            max_right: int that represents the maximum right x point that can
                be reached

        Return:
            x_landing: An int that represents the x coord of the landing
                point of the player the game will use to generate the
                platform
        """
        # Account for difficulty. Harder difficulties will have the
        # minimum increased
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
        return x_landing

    def calculate_platform_center_x(
        self, x_landing, new_platform_width, center
    ):
        """
        Calculates the x coord of the center of the new platform

        Args:
            x_landing: An int that represents the x coord of the landing
                point of the player the game will use to generate the
                platform
            new_platform_width: An int that represents the width of the
                new platform
            center: A tuple representing the center of the old platform
        """
        # Check if player needs to jump left or right of current platform
        if x_landing < center[0]:
            is_left = True
        else:
            is_left = False
        half_width = math.ceil(new_platform_width / 2)
        # Calculate center of new platform
        if is_left:
            new_platform_center_x = x_landing + half_width
        else:
            new_platform_center_x = x_landing - half_width

        # If the center is out of bounds, set it so its within bounds
        if new_platform_center_x - half_width < 0:
            new_platform_center_x = half_width
        if new_platform_center_x + half_width > self._screen_width:
            new_platform_center_x = self._screen_width - half_width

        return int(new_platform_center_x)

    def calculate_platform_center_y(
        self,
        reach_max,
        x_landing,
        max_y_height,
        center,
        velocity_x_max,
        new_platform_height,
    ):
        """
        Calculates the y coord of the center of the new platform

        Args:
            reach_max: A tuple that represents the bounds in which the
                player can obtain the maximum height
            x_landing: An int that represents the x coord of the landing
                point of the player the game will use to generate the
                platform
            max_y_height: A float representing maximum height that the
                player can reach
            center: A tuple representing the center of the old platform
            velocity_x_max: A float representing the maximum velocity
                that the player can reach based on the length of the
                previous platform
            new_platform_height: An int representing the height of
                the new platform

        Returns:
            An int, new_platform_center_y that represents the y coord
                of the new platform
        """
        # Check if landing is in range of where max height is reachable.
        # If not, calculate max reachable y
        if x_landing > reach_max[0] or x_landing < reach_max[1]:
            max_y_reach = max_y_height
        else:
            if x_landing < reach_max[0]:
                x_distance = reach_max[0] - x_landing
            else:
                x_distance = x_landing - reach_max[1]
            time = x_distance / velocity_x_max
            max_y_reach = max_y_height - 0.5 * self._gravity.y * time**2
        max_y_reach = int(max_y_reach)
        max_y_reach_point = center[1] - max_y_reach

        # Adjust difficulty level
        minimum_y = center[1] - max_y_reach + 1

        new_platform_center_y = (
            random.randint(max_y_reach_point, minimum_y)
            + new_platform_height / 2
        )
        return new_platform_center_y

    def set_difficulty(self, difficulty):
        """
        Sets the difficulty of the game

        Args:
            difficulty: float indicating the difficulty of the game
                1 is hard, 0.75 is medium, 0.5 is easy
        """
        self._game_difficulty = difficulty

    def increase_score(self):
        """
        Increases the private attribute _score by 1

        Args:
            none
        """
        self._score += 1

    @property
    def player(self):
        """
        Allows private attribute _player to be output

        Args:
            none

        Returns:
            The player attribute of the model.
        """
        return self._player

    @property
    def platforms(self):
        """
        Allows private attribute platforms to be accessed

        Args:
            none

        Returns:
            The platforms attribute of the model.
        """
        return self._platforms

    @property
    def score(self):
        """
        Allows private attribute score to be accessed

        Args:
            none

        Returns:
            The score attribute
        """
        return self._score

    @property
    def game_over(self):
        """
        Allows private attribute _game_over to be accessed

        Args:
            none

        Return:
            A boolean representing if game is over
        """
        return self._game_over


class Platform(pygame.sprite.Sprite):
    """
    Creates a platform for a sprite to interact with.

    Attributes:
        _surf: A pygame.Surface() object that represents the surface of the
            platform
        _rect: A pygame.Rect() object that represents the rect of the
            platform
        _color: A tuple representing the RGB color of the platform
    """

    def __init__(self, surf, center, color=(128, 128, 128)) -> None:
        """
        Initializes the platforms.

        Args:
            surf: A surface representing platforms
            center: A tuple representing the center of the platform location
            color: A tuple representing the platform RGB color code. Defaults to
                (128, 128, 128).
        """
        super().__init__()
        self._surf = surf
        self._color = color
        self._surf.fill(color)
        self._center = center
        self._rect = self._surf.get_rect(center=center)

    def set_rect(self, x_pos, y_pos):
        """
        Sets the rect of the platform.

        Args:
            x_pos: An int representing the x location of the platform sprite.
            y_pos: An int representing the y location of the platform sprite.
        """
        self._rect.x = x_pos
        self._rect.y = y_pos

    @property
    def rect(self):
        """
        Allows private attribute _rect to be accessed

        Args:
            none

        Returns:
            The rectangle attribute of the model.
        """
        return self._rect

    @property
    def surf(self):
        """
        Allows private attribute _Surf to be accessed

        Args:
            none

        Returns:
            The surface attribute of the model.
        """
        return self._surf


class Player:
    """
    A class to generate and dictate actions of the game
    character sprite.

    Attributes:
        _gravity: A pygame.math.Vector2() that stores the gravity of
             the game
        _friction: An int representing the value friction associated
            with the characters interactions with objects in game
        _jump_velocity: An int representing the jump velocity of
            the player
        _acceleration: A pygame.math.Vector2() representing the
            acceleration acting on the character in any direction.
        _velocity: A pygame.math.Vector2() representing the current
            velocity of the character
        _position: A pygame.math.Vector2() representing the position
            of the character in the game
        _image: A pygame.Surface() object that represents the default
            surface size of the player
        _rect: A pygame.Rect() object that represents the player sprite
            hitbox
    """

    def __init__(self, gravity, friction) -> None:
        """
        Initializes the character.

        Args:
            gravity: A pygame.math.Vector2() that stores the gravity of
                the game
            friction: A float representing the friction between character
                and platforms
        """
        self._gravity = gravity
        self._friction = friction
        self._jump_velocity = -10
        self._acceleration = VECTOR(0, 0)
        self._velocity = VECTOR(0, 0)
        self._position = VECTOR(200, 310)
        self._character_width = 35
        self._image = pygame.image.load("sprites/TestRocket.png")
        self._image = pygame.transform.scale(
            self._image,
            (
                self._character_width,
                self._character_width
                * (self._image.get_height() / self._image.get_width()),
            ),
        )
        self._rect = self._image.get_rect(center=self._position)

    def update(self):
        """
        Updates the character rect based on position

        Args:
            none
        """
        self._rect = self._image.get_rect(center=self._position)

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
        Dictates the motion of the player sprite.

        Args:
            x_acceleration: A float representing horizontal
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
        Returns the players jump velocity, dependent on
        whether or not player is jumping

        Args:
            none

        Returns:
            _velocity as an int representing the y
            velocity the player is set to when jumping
        """
        return self._jump_velocity

    @property
    def acceleration(self):
        """
        Allows the acceleration of player to be accessed

        Args:
            none

        Returns:
            _acceleration of player in form of float
        """
        return self._acceleration

    @property
    def velocity(self):
        """
        Allows the velocity of player to be accessed

        Args:
            none

        Returns
            _velocity of player in form of float
        """
        return self._velocity

    @property
    def position(self):
        """
        Allows the position of the player to be accessed

        Args:
            none

        Returns:
            The _position attribute of the model.
        """
        return self._position

    @property
    def image(self):
        """
        Returns the image sprite surface of the player

        Args:
            none

        Return:
            pygame.Surface() that is the sprite of the
            player
        """
        return self._image

    @property
    def rect(self):
        """
        Allows the rectangle object of the player to be accessed

        Args:
            none

        Returns:
            The _rect private attribute of the model, pygame.Surface
            object
        """
        return self._rect
