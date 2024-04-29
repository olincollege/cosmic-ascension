from model import Model, Platform, Player
import pygame
import pytest
from test_common import (
    check_private_var,
    check_class_attribute,
    check_class_property,
    check_core_method,
)

# Test cases for Model

model_update = []

model_platform_generation = []


# Check that score correctly increases by 1
def test_increase_score():
    """
    Checks that the increase_score method correctly increments the score by 1 when run.

    Args:
        none
    """
    instance = Model(0, 0, 0)
    instance.increase_score()
    exp_score = instance.score

    # Check correct type and iteration
    assert isinstance(exp_score, int)
    assert exp_score == 1
