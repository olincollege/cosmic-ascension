from controller import Controller
import pygame
import pytest
from pygame.locals import *

# Test cases

controller_updates = [
    # Check if the left arrow event returns correct movement
    (
        pygame.event.Event(
            pygame.KEYDOWN,
            {
                "mod": 0,
                "scancode": 30,
                "key": pygame.K_LEFT,
                "unicode": "left arrow",
            },
        ),
        -0.5,
        False,
    ),
    # Check if the right arrow event returns correct movement
    (
        pygame.event.Event(
            pygame.KEYDOWN,
            {
                "mod": 0,
                "scancode": 30,
                "key": pygame.K_RIGHT,
                "unicode": "right arrow",
            },
        ),
        0.5,
        False,
    ),
    # Check if the space bar event returns correct movement
    (
        pygame.event.Event(
            pygame.KEYDOWN,
            {
                "mod": 0,
                "scancode": 30,
                "key": pygame.K_SPACE,
                "unicode": "space",
            },
        ),
        0.0,
        True,
    ),
    # Check if left arrow is released movement halts
    (
        pygame.event.Event(
            pygame.KEYUP,
            {
                "mod": 0,
                "scancode": 30,
                "key": pygame.K_LEFT,
                "unicode": "left arrow",
            },
        ),
        0.0,
        False,
    ),
    # Check if right arrow is released movement halts
    (
        pygame.event.Event(
            pygame.KEYUP,
            {
                "mod": 0,
                "scancode": 30,
                "key": pygame.K_RIGHT,
                "unicode": "right arrow",
            },
        ),
        0.0,
        False,
    ),
    # Check if space bar is released movement halts
    (
        pygame.event.Event(
            pygame.KEYUP,
            {
                "mod": 0,
                "scancode": 30,
                "key": pygame.K_SPACE,
                "unicode": "space",
            },
        ),
        0.0,
        False,
    ),
]


@pytest.mark.parametrize("keystroke,x_move,y_move", controller_updates)
def test_controller_updates(keystroke, x_move, y_move):
    """
    Tests that a specified keystroke in the events queue will return the
    correct set of movements.

    Args:
        keystroke: A pygame event representing a simulated pressed
            key from the user.
        x_move: A float representing the expected movement when pressing a key.
        y_move: A bool representing the expected jump status when
            pressing a key.
    """
    pygame.init()
    instance = Controller(None)
    # post the event
    pygame.event.post(keystroke)
    instance.update_game()

    x_move_result = instance.left_right
    y_move_result = instance.jumping

    # Check the correct type
    assert isinstance(x_move_result, float)
    assert isinstance(y_move_result, bool)

    # Check the correct value result
    assert x_move_result == x_move
    assert y_move_result == y_move
