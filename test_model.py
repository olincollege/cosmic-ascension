"""
This module contains unit tests for classes found in model.py.

Not tested:
    Model:
        update:
        set_difficulty: setter function, uneccessary to test
    Platform:
        set_rect: setter function, uneccessary to test
    Player:
        update:
        set_position: setter function, uneccessary to test
        set_velocity: setter function, uneccessary to test
"""

import pygame
import pytest
from model import Model, Player

pygame.init()
VECTOR = pygame.math.Vector2

# Test cases for Model

model_update = []

model_platform_generation = []

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
