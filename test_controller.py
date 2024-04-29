from controller import Controller
from test_common import (
    check_private_var,
    check_class_attribute,
    check_class_property,
    check_core_method,
)
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
            {"mod": 0, "scancode": 30, "key": pygame.K_SPACE, "unicode": "space"},
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
            {"mod": 0, "scancode": 30, "key": pygame.K_SPACE, "unicode": "space"},
        ),
        0.0,
        False,
    ),
]

# private_properties = [
#     (
#         check_private_var(
#             Controller,
#         )
#     )
# ]


@pytest.mark.parametrize("keystroke,x_move,y_move", controller_updates)
def test_controller_updates(keystroke, x_move, y_move):
    """
    Tests that a specified keystroke in the events queue will return the
    correct set of movements.

    Args:
        keystroke: A pygame event representing a simulated pressed key from the user.
        x_move: A float representing the expected movement when pressing a key.
        y_move: A bool representing the expected jump status when pressing a key.
    """
    pygame.init()
    instance = Controller()
    # post the event
    pygame.event.post(keystroke)
    instance.update()

    x_move_result = instance.left_right
    y_move_result = instance.jumping

    # Check the correct type
    assert isinstance(x_move_result, float)
    assert isinstance(y_move_result, bool)

    # Check the correct value result
    assert x_move_result == x_move
    assert y_move_result == y_move


# @pytest.mark.parametrize(
#     "func",
#     [
#         check_private_var,
#         check_class_attribute,
#         check_class_property,
#         check_core_method,
#     ],
# )


# @pytest.mark.parametrize("private")
# def test_private_property():
#     instance = Controller()

#     # Get all variables and methods of the class
#     var_list = [
#         obj
#         for obj in dir(instance)
#         if not obj.startswith("__") and not callable(getattr(instance, obj))
#     ]

#     for var in var_list:
#         # Check that all attributes are private
#         assert check_private_var(instance, var)
#         # Check that all attributes have a property
#         assert check_class_property(Controller, var[1:])

#     # Check th


# Checks to run:
# private: jumping, dead, left_right
# property: all of the above
