from view import View
import pygame
import pytest
from test_common import (
    check_private_var,
    check_class_attribute,
    check_class_property,
    check_core_method,
)

# Cannot test draw method, as it is a visual display
# Cannot test score method, as it is a visual


# Check for common features
def test_private_variable():
    # Check that there is 1 private variable
    assert check_private_var(View)
    # Check that there is a draw method (necessary for view)
    assert check_core_method(View, "draw")
