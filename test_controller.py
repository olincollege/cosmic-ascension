from test_common import (
    check_private_var,
    check_board_attribute,
    check_board_property,
    check_board_assignment,
    check_core_method,
    check_abstract_method,
)


@pytest.mark.parametrize(
    "func",
    [
        check_private_board,
        check_board_attribute,
        check_board_property,
        check_board_assignment,
        check_core_method,
        check_abstract_method,
    ],
)

# Checks to run: 
# private: velocity, model, acceleration
# move method: left, right, and jump velocities
# jump method: hitting a platform and not hitting one