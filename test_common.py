def _is_private_variable(class_name, var_name):
    """
    Check if a variable name is private in a class.

    Given a class and variable name, check whether that variable name is a
    private variable. A variable name is considered private if it begins with
    exactly one underscore (_) and is not a class-private variable (in the form
    _Class__var).

    Args:
        class_name: A class used to derive the comparison string for the
            class-private variable name.
        var_name: A string representing the variable name.

    Returns:
        True if var_name is a private variable in class_name and False
        otherwise.
    """
    return (
        var_name.startswith("_")
        and not var_name.startswith("__")
        and not var_name.startswith(f"_{class_name.__name__}")
    )


def check_private_var(class_name, _):
    """
    Check whether a class has at least one private variable.

    Private variables are determined as defined in the _is_private_variable
    function.

    Args:
        class_name: A class to check for private variables.

    Returns:
        True if the class has at least one private variable and False otherwise.
    """
    game = Game()
    instance = class_name(game)
    private_variables = [
        attr for attr in dir(instance) if _is_private_variable(class_name, attr)
    ]
    return len(private_variables) >= 1


def check_board_attribute(class_name, _):
    """
    Check whether a class has an attribute called "board".

    Args:
        class_name: A class to check for the board attribute.
    """
    return hasattr(class_name, "board")


def check_board_property(class_name, _):
    """
    Check whether TicTacToeView has a property called board (created with the
    property decorator).

    Args:
        class_name: A class to check for the board property.
    """
    return isinstance(class_name.board, property)


def check_core_method(class_name, method_name):
    """
    Check that a class has a method.

    Args:
        class_name: A class to check.
        method_name: A string representing the method name to check for.
    """
    return hasattr(class_name, method_name)