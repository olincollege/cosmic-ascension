from model import Model, Platform, Player
import pygame
import pytest
import math

vector = pygame.math.Vector2

# Test cases for Model

model_update = []

model_platform_generation = []

model_check_player_off_screen = [
    # Window is width 400 height 450
    # Check that a position to the left is considered off screen and ends game
    (vector(-10, 100), True),
    # Check that a position to the right of the screen is considered off screen
    # and ends game
    (vector(410, 100), True),
    # Check that a position in the window doesn't end the game
    (vector(350, 100), False),
]

model_set_difficulty = [
    # Check that hard mode implements correctly
    (1.0, 1.0),
    # Check that medium implements correctly
    (0.75, 0.75),
    # Check that easy implements correctly
    (0.5, 0.5),
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


@pytest.mark.parametrize("in_difficulty,out_difficulty", model_set_difficulty)
def test_set_difficulty(in_difficulty, out_difficulty):
    instance = Model(0, 400, 450)

    # Set the difficulty
    instance.set_difficulty(in_difficulty)

    # Get result
    exp_difficulty = instance.game_difficulty

    assert isinstance(exp_difficulty, float)
    assert out_difficulty == exp_difficulty


# Player test cases

player_set_velocity = [
    # Check that a zero velocity returns correctly
    (vector(0, 0), [0, 0]),
    # Check that a horizontal velocity returns correctly
    (vector(1, 0), [1, 0]),
    # Check that a vertical velocity returns correctly
    (vector(0, 1), [0, 1]),
    # Check that a negative horizontal velocity returns correctly
    (vector(-1, 0), [-1, 0]),
    # Check that a negative vertical velocity returns correctly
    (vector(0, -1), [0, -1]),
    # Check that velocity in both horizontal and vertical returns correctly
    (vector(1, 1), [1, 1]),
    # Check that negative velocity in both direction returns correctly
    (vector(-1, -1), [-1, -1]),
    # Check that a negative x and pos y returns correctly
    (vector(1, -1), [1, -1]),
    # Check that a negative x and pos y returns correctly
    (vector(-1, 1), [-1, 1]),
]


@pytest.mark.parametrize("in_velocity,out_velocity", player_set_velocity)
def test_set_velocity(in_velocity, out_velocity):
    instance = Player(10, 0.12)
    instance.set_velocity(in_velocity)
    exp_velocity = instance.velocity
    assert exp_velocity == out_velocity
