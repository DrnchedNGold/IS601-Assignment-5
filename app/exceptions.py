# Author: Varun Sabbineni 10/6/2025
# Exception Hierarchy

class CalculatorError(Exception):
    """
    Base exception for all calculator-specific errors.

    This is the parent class for all our custom exceptions. By having a common
    base class, we can catch "any calculator error" with a single except clause
    if we want to, or catch specific types individually.

    This is a common pattern in Python - create your own exception hierarchy
    that inherits from Exception, making it easy to distinguish your application's
    errors from built-in Python errors.
    """
    pass


class ValidationError(CalculatorError):
    """
    Raised when user input doesn't pass validation checks.

    This exception happens when someone enters something invalid - like typing
    letters instead of numbers, entering a number that's too large, or providing
    input in the wrong format. It's our way of saying "hold on, that input
    doesn't look right."

    By having a specific exception for validation issues, we can handle them
    differently than other errors - maybe showing a helpful message to the user
    about what format we expect.
    """
    pass


class OperationError(CalculatorError):
    """
    Raised when something goes wrong during a calculation.

    This exception covers problems that happen while actually doing math - things
    like dividing by zero, trying to take the square root of a negative number,
    or using an operation that doesn't exist.

    These are different from validation errors because the input might be valid,
    but the mathematical operation itself can't be completed for some reason.
    """
    pass


class ConfigurationError(CalculatorError):
    """
    Raised when the calculator's settings are invalid.

    This exception happens when there's a problem with how the calculator is
    configured - like an invalid file path, a negative history size, or a
    missing required setting.

    Configuration errors are caught early (usually during startup) so we can
    alert the user to fix the settings before trying to use the calculator.
    """
    pass