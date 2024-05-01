"""
This module contains unit tests for classes found in model.py.

Not tested:
    Model:
        update: uses built in pygames functions and other tested functions,
            uneccessary to test
        set_difficulty: setter function, uneccessary to test
    Platform:
        set_rect: setter function, uneccessary to test
    Player:
        update: runs built in pygame function, uneccessary to test
        set_position: setter function, uneccessary to test
        set_velocity: setter function, uneccessary to test
"""

import math
import pygame
import pytest
from model import Model, Player, Platform

pygame.init()
VECTOR = pygame.math.Vector2

# Test cases for Model


model_check_player_off_screen = [
    # Window is width 400 height 450
    # Check that a position to the left is considered off screen and ends game
    (VECTOR(-10, 100), True),
    # Check that a position to the right of the screen is considered off screen
    # and ends game
    (VECTOR(410, 100), True),
    # Check that a position in the window doesn't end the game
    (VECTOR(350, 100), False),
]


# Check that score correctly increases by 1
def test_increase_score():
    """
    Checks that the increase_score method correctly increments the score by
    1 when run.

    Args:
        none
    """
    instance = Model(0, 400, 450)
    instance.increase_score()
    exp_score = instance.score

    # Check correct type and iteration
    assert isinstance(exp_score, int)
    assert exp_score == 1


@pytest.mark.parametrize("position,end_game", model_check_player_off_screen)
def test_check_player_off_screen(position, end_game):
    """
    Checks that the check_player_off_screen method correctly registers when
    the sprite has left the game window and reports the game as over.

    Args:
        position: A vector tuple representing the players x and y position
        end_game: A bool representing the expected value of whether the
            game is over or not depending on the position.
    """
    # Set Model
    instance = Model(0, 400, 450)

    # Set position
    instance.player.set_position(position)

    # Get result
    instance.check_player_off_screen()
    exp_output = instance.game_over

    assert isinstance(exp_output, bool)
    assert exp_output == end_game


def test_platform_generation_easy():
    """
    Checks that all platforms generated are on screen in easy
    difficulty, that no platforms collide with each other, and
    all platforms are reachable
    """
    # Set ground this is the same across all game modes
    ground = Platform(surf=pygame.Surface((200, 20)), center=(200, 445))
    platforms = pygame.sprite.Group()
    platforms.add(ground)

    instance = Model(platforms, 400, 450)
    instance.set_difficulty(0.5)
    instance.platform_generation()
    for i in range(1, len(instance.platforms)):
        # Get current platform
        platform = instance.platforms.sprites()[i]
        # Check with among the group of platforms how platforms this
        # platform collides with. Should be only 1 as it collides
        # with itself
        collided_sprites = pygame.sprite.spritecollide(
            platform, instance.platforms, False
        )

        # Get previous platform dimensions
        latest_platform = i - 1
        previous_platform = instance.platforms.sprites()[latest_platform]
        left = previous_platform.rect.left
        right = previous_platform.rect.right

        # Gravity
        gravity = 0.35

        # Calculate the maximum x velocity the player can reach based
        # on how long the previous platform is
        velocity_x_max = math.sqrt(2 * 0.5 * (right - left))

        # Calculate maximum height player can reach accounting for difficulty
        max_y_height = 0.5 * (
            ((-instance.player.jump_velocity) ** 2) / (2 * gravity)
        )

        # Calculate how long it takes to fall from this height
        fall_time = math.sqrt(2 * max_y_height / gravity)

        # Calculate how far player can move in that time
        max_x_distance = int(velocity_x_max * fall_time)
        # Accounting for difficulty level
        max_x_distance = max_x_distance * 0.5

        # Accounting for take off and landing of player. Gives
        # more leeway at higher difficult to account for reaction
        # time. Can't expect player to make perfect jump to
        # maximize height and distance every time
        max_x_distance -= instance.player.rect.width * 1.5 * 0.5

        # Distance between platforms if the current platform is left of
        # the previous platform
        x_travel_distance_if_left_of = right - platform.rect.left
        # Distance between platforms if the current platform is right of
        # the previous platform
        x_travel_distance_if_right_of = left - platform.rect.right

        # Calculate y travel distance
        y_travel_distance = previous_platform.rect.top - platform.rect.bottom

        # Check that the platform left bound is not over the screen bound
        assert (
            platform.rect.left >= 0
        ), f"out of bounds: {platform.rect.left} >= 0"
        # Check that the platform right bound is not over the screen bound
        assert (
            platform.rect.right <= 400
        ), f"out of bounds: {platform.rect.right} <= 400"
        # Check that the platform does not collide with more than itself
        assert not len(collided_sprites) > 1, "collision"
        # Check if the travel distance is within the max x distance.
        # The "or" is there because as long as the platform is reachable
        # from one side of the platform, it is fine
        assert (
            x_travel_distance_if_left_of <= max_x_distance
            or x_travel_distance_if_right_of <= max_x_distance
        ), (
            f"x distance: {x_travel_distance_if_left_of} <= {max_x_distance},"
            f" {x_travel_distance_if_right_of} <= {max_x_distance}"
        )
        # Check that the y travel distance is less than the max y height
        assert (
            y_travel_distance <= max_y_height
        ), f"y distance: {y_travel_distance} <= {max_y_height}"


def test_platform_generation_medium():
    """
    Checks that all platforms generated are on screen in medium
    difficulty, that no platforms collide with each other, and
    all platforms are reachable
    """
    # Set ground this is the same across all game modes
    ground = Platform(surf=pygame.Surface((200, 20)), center=(200, 445))
    platforms = pygame.sprite.Group()
    platforms.add(ground)

    instance = Model(platforms, 400, 450)
    instance.set_difficulty(0.75)
    instance.platform_generation()
    for i in range(1, len(instance.platforms)):
        # Get current platform
        platform = instance.platforms.sprites()[i]
        # Check with among the group of platforms how platforms this
        # platform collides with. Should be only 1 as it collides
        # with itself
        collided_sprites = pygame.sprite.spritecollide(
            platform, instance.platforms, False
        )

        # Get previous platform dimensions
        latest_platform = i - 1
        previous_platform = instance.platforms.sprites()[latest_platform]
        left = previous_platform.rect.left
        right = previous_platform.rect.right

        # Gravity
        gravity = 0.35

        # Calculate the maximum x velocity the player can reach based
        # on how long the previous platform is
        velocity_x_max = math.sqrt(2 * 0.5 * (right - left))

        # Calculate maximum height player can reach accounting for difficulty
        max_y_height = 0.75 * (
            ((-instance.player.jump_velocity) ** 2) / (2 * gravity)
        )

        # Calculate how long it takes to fall from this height
        fall_time = math.sqrt(2 * max_y_height / gravity)

        # Calculate how far player can move in that time
        max_x_distance = int(velocity_x_max * fall_time)
        # Accounting for difficulty level
        max_x_distance = max_x_distance * 0.75

        # Accounting for take off and landing of player. Gives
        # more leeway at higher difficult to account for reaction
        # time. Can't expect player to make perfect jump to
        # maximize height and distance every time
        max_x_distance -= instance.player.rect.width * 1.5 * 0.75

        # Distance between platforms if the current platform is left of
        # the previous platform
        x_travel_distance_if_left_of = right - platform.rect.left
        # Distance between platforms if the current platform is right of
        # the previous platform
        x_travel_distance_if_right_of = left - platform.rect.right

        # Calculate y travel distance
        y_travel_distance = previous_platform.rect.top - platform.rect.bottom

        # Check that the platform left bound is not over the screen bound
        assert (
            platform.rect.left >= 0
        ), f"out of bounds: {platform.rect.left} >= 0"
        # Check that the platform right bound is not over the screen bound
        assert (
            platform.rect.right <= 400
        ), f"out of bounds: {platform.rect.right} <= 400"
        # Check that the platform does not collide with more than itself
        assert not len(collided_sprites) > 1, "collision"
        # Check if the travel distance is within the max x distance.
        # The "or" is there because as long as the platform is reachable
        # from one side of the platform, it is fine
        assert (
            x_travel_distance_if_left_of <= max_x_distance
            or x_travel_distance_if_right_of <= max_x_distance
        ), (
            f"x distance: {x_travel_distance_if_left_of} <= {max_x_distance},"
            f" {x_travel_distance_if_right_of} <= {max_x_distance}"
        )
        # Check that the y travel distance is less than the max y height
        assert (
            y_travel_distance <= max_y_height
        ), f"y distance: {y_travel_distance} <= {max_y_height}"


def test_platform_generation_hard():
    """
    Checks that all platforms generated are on screen in hard
    difficulty, that no platforms collide with each other, and
    all platforms are reachable
    """
    # Set ground this is the same across all game modes
    ground = Platform(surf=pygame.Surface((200, 20)), center=(200, 445))
    platforms = pygame.sprite.Group()
    platforms.add(ground)

    instance = Model(platforms, 400, 450)
    instance.set_difficulty(1)
    instance.platform_generation()
    for i in range(1, len(instance.platforms)):
        # Get current platform
        platform = instance.platforms.sprites()[i]
        # Check with among the group of platforms how platforms this
        # platform collides with. Should be only 1 as it collides
        # with itself
        collided_sprites = pygame.sprite.spritecollide(
            platform, instance.platforms, False
        )

        # Get previous platform dimensions
        latest_platform = i - 1
        previous_platform = instance.platforms.sprites()[latest_platform]
        left = previous_platform.rect.left
        right = previous_platform.rect.right

        # Gravity
        gravity = 0.35

        # Calculate the maximum x velocity the player can reach based
        # on how long the previous platform is
        velocity_x_max = math.sqrt(2 * 0.5 * (right - left))

        # Calculate maximum height player can reach accounting for difficulty
        max_y_height = 1 * (
            ((-instance.player.jump_velocity) ** 2) / (2 * gravity)
        )

        # Calculate how long it takes to fall from this height
        fall_time = math.sqrt(2 * max_y_height / gravity)

        # Calculate how far player can move in that time
        max_x_distance = int(velocity_x_max * fall_time)
        # Accounting for difficulty level
        max_x_distance = max_x_distance * 1

        # Accounting for take off and landing of player. Gives
        # more leeway at higher difficult to account for reaction
        # time. Can't expect player to make perfect jump to
        # maximize height and distance every time
        max_x_distance -= instance.player.rect.width * 1.5 * 1

        # Distance between platforms if the current platform is left of
        # the previous platform
        x_travel_distance_if_left_of = right - platform.rect.left
        # Distance between platforms if the current platform is right of
        # the previous platform
        x_travel_distance_if_right_of = left - platform.rect.right

        # Calculate y travel distance
        y_travel_distance = previous_platform.rect.top - platform.rect.bottom

        # Check that the platform left bound is not over the screen bound
        assert (
            platform.rect.left >= 0
        ), f"out of bounds: {platform.rect.left} >= 0"
        # Check that the platform right bound is not over the screen bound
        assert (
            platform.rect.right <= 400
        ), f"out of bounds: {platform.rect.right} <= 400"
        # Check that the platform does not collide with more than itself
        assert not len(collided_sprites) > 1, "collision"
        # Check if the travel distance is within the max x distance.
        # The "or" is there because as long as the platform is reachable
        # from one side of the platform, it is fine
        assert (
            x_travel_distance_if_left_of <= max_x_distance
            or x_travel_distance_if_right_of <= max_x_distance
        ), (
            f"x distance: {x_travel_distance_if_left_of} <= {max_x_distance},"
            f" {x_travel_distance_if_right_of} <= {max_x_distance}"
        )
        # Check that the y travel distance is less than the max y height
        assert (
            y_travel_distance <= max_y_height
        ), f"y distance: {y_travel_distance} <= {max_y_height}"


# Player test cases

player_move = [
    # Check that when the player is not moving their position remains same
    # on platform
    (0, False, True, [200, 310]),
    # off platform (gravity)
    (0, False, False, [200, 325]),
    # Check when the player is moving left and not jumping
    # on platform
    (-0.5, False, True, [199.25, 310]),
    # off platform
    (-0.5, False, False, [199.25, 325]),
    # Check when the player is moving right and not jumping
    # on platform
    (0.5, False, True, [200.75, 310]),
    # off platform
    (0.5, False, False, [200.75, 325]),
    # Check when player is moving left and jumping on platform
    # (not possible to jump off platform)
    (-0.5, True, True, [199.25, 295]),
    # Check when player is moving right and jumping
    (0.5, True, True, [200.75, 295]),
    # Check when a player is not moving horizontally and jumping
    (0, True, True, [200, 295]),
]


@pytest.mark.parametrize(
    "x_accel,jumping,on_platform,out_position", player_move
)
def test_move(x_accel, jumping, on_platform, out_position):
    """
    Checks whether the move method correctly sets the player position
    calculated with the x acceleration and jumping velocity.

    Args:
        x_accel: A float representing the horizontal acceleration
        jumping: A bool representing if the character is jumping or not
        on_platform: A bool representing if the character is on a platform
            or not. This dictates influence of gravity.
        out_position: A pygame vector representing the expected x and
            y position of player after move method
    """
    if on_platform:
        y_velocity = 0
    else:
        y_velocity = 10

    if jumping:
        y_velocity -= 10

    instance = Player(VECTOR(0, y_velocity), 0.12)
    instance.move(x_accel)
    exp_position = instance.position

    assert exp_position == out_position
