# Author: Varun Sabbineni 9/30/2025
# tests/test_operations.py

"""
Unit tests for the Operation class and its arithmetic methods.

This file tests all the basic math operations to make sure they work correctly.
We use pytest's parameterize feature for some tests to avoid repeating code,
and we also test error cases like dividing by zero.

The tests follow the AAA pattern: Arrange (set up), Act (run the code), Assert (check results).
"""

import pytest
from typing import Union
from app.operation import Operation

# Type alias to make it clear we accept both integers and floats
Number = Union[int, float]

# -----------------------------------------------------------------------------------
# Addition Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),           # Two positive numbers
        (0, 0, 0),           # Both zeros
        (-1, 1, 0),          # Negative plus positive
        (2.5, 3.5, 6.0),     # Decimal numbers
        (-2.5, 3.5, 1.0),    # Negative decimal plus positive decimal
    ],
    ids=[
        "add_two_positive_integers",
        "add_two_zeros",
        "add_negative_and_positive",
        "add_two_floats",
        "add_negative_and_positive_floats",
    ]
)
def test_addition(a: Number, b: Number, expected: Number) -> None:
    """
    Tests that the addition method correctly adds different types of numbers.
    
    Parameterized testing lets us run the same test logic with multiple inputs,
    which saves us from writing the same test over and over. Each set of parameters
    gets its own test ID so we can see which specific case failed if something breaks.
    
    Parameters:
    - a: First number to add
    - b: Second number to add
    - expected: What the result should be
    """
    # Act - perform the addition
    result = Operation.addition(a, b)
    
    # Assert - verify the result matches what we expect
    assert result == expected, f"Expected {a} + {b} to equal {expected}, but got {result}"

def test_addition_with_zero():
    """
    Tests that adding zero to a number returns the original number.
    
    This is a basic property of addition (the identity property), so it's worth
    verifying explicitly even though it's covered in the parameterized tests.
    """
    # Arrange
    a = 10.0
    b = 0.0
    expected_result = 10.0

    # Act
    result = Operation.addition(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, got {result}"

# -----------------------------------------------------------------------------------
# Subtraction Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),           # Subtracting smaller from larger
        (0, 0, 0),           # Both zeros
        (-5, -3, -2),        # Two negative numbers
        (10.5, 5.5, 5.0),    # Positive decimals
        (-10.5, -5.5, -5.0), # Negative decimals
    ],
    ids=[
        "subtract_positive_numbers",
        "subtract_zeros",
        "subtract_negative_numbers",
        "subtract_positive_floats",
        "subtract_negative_floats",
    ]
)
def test_subtraction(a: Number, b: Number, expected: Number) -> None:
    """
    Tests that subtraction works correctly with various number combinations.
    
    Subtraction can be tricky with negative numbers, so we test several scenarios
    to ensure the method handles them all properly.
    
    Parameters:
    - a: Number to subtract from
    - b: Number to subtract
    - expected: Expected result
    """
    # Act
    result = Operation.subtraction(a, b)
    
    # Assert
    assert result == expected, f"Expected {a} - {b} to equal {expected}, but got {result}"

def test_subtraction_positive_negative():
    """
    Tests subtracting a negative number from a positive number.
    
    When you subtract a negative, it's actually like adding a positive (double negative),
    so this test verifies that math rule works correctly.
    """
    # Arrange
    a = 10.0
    b = -5.0
    expected_result = 15.0

    # Act
    result = Operation.subtraction(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} - ({b}) to be {expected_result}, got {result}"

# -----------------------------------------------------------------------------------
# Multiplication Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),           # Two positive integers
        (0, 10, 0),          # Multiplying by zero
        (-2, -3, 6),         # Two negatives make a positive
        (2.5, 4.0, 10.0),    # Decimal multiplication
        (-2.5, 4.0, -10.0),  # Negative times positive
    ],
    ids=[
        "multiply_positive_integers",
        "multiply_by_zero",
        "multiply_two_negatives",
        "multiply_floats",
        "multiply_negative_and_positive",
    ]
)
def test_multiplication(a: Number, b: Number, expected: Number) -> None:
    """
    Tests multiplication with different number types and signs.
    
    Multiplication has some interesting properties - like how two negatives make
    a positive, and how anything times zero equals zero. We test all these cases.
    
    Parameters:
    - a: First number to multiply
    - b: Second number to multiply
    - expected: Expected product
    """
    # Act
    result = Operation.multiplication(a, b)
    
    # Assert
    assert result == expected, f"Expected {a} * {b} to equal {expected}, but got {result}"

def test_multiplication_with_zero():
    """
    Explicitly tests that multiplying any number by zero gives zero.
    
    This is a fundamental property of multiplication, and while it's in the
    parameterized tests, having a dedicated test makes it extra clear.
    """
    # Arrange
    a = 10.0
    b = 0.0
    expected_result = 0.0

    # Act
    result = Operation.multiplication(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, got {result}"

# -----------------------------------------------------------------------------------
# Division Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),           # Simple positive division
        (-6, -3, 2.0),         # Two negatives cancel out
        (6.0, 3.0, 2.0),       # Decimal division
        (-6.0, 3.0, -2.0),     # Negative divided by positive
        (0, 5, 0.0),           # Zero divided by anything is zero
    ],
    ids=[
        "divide_positive_numbers",
        "divide_negative_numbers",
        "divide_floats",
        "divide_negative_by_positive",
        "divide_zero_by_number",
    ]
)
def test_division(a: Number, b: Number, expected: float) -> None:
    """
    Tests division with various number combinations.
    
    Division is more complex than other operations because we have to handle
    the special case of dividing by zero (which is tested separately).
    
    Parameters:
    - a: Dividend (number being divided)
    - b: Divisor (number we're dividing by)
    - expected: Expected quotient
    """
    # Act
    result = Operation.division(a, b)
    
    # Assert
    assert result == expected, f"Expected {a} / {b} to equal {expected}, but got {result}"

def test_division_with_zero_numerator():
    """
    Tests that zero divided by any non-zero number equals zero.
    
    This is an important edge case - zero divided by something is always zero,
    but something divided by zero is an error (tested below).
    """
    # Arrange
    a = 0.0
    b = 5.0
    expected_result = 0.0

    # Act
    result = Operation.division(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, got {result}"

# -----------------------------------------------------------------------------------
# Division by Zero Tests (Error Cases)
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b",
    [
        (1, 0),    # Positive number divided by zero
        (-1, 0),   # Negative number divided by zero
        (0, 0),    # Zero divided by zero
    ],
    ids=[
        "divide_positive_by_zero",
        "divide_negative_by_zero",
        "divide_zero_by_zero",
    ]
)
def test_division_by_zero(a: Number, b: Number) -> None:
    """
    Tests that dividing by zero raises a ValueError with the correct message.
    
    This is a negative test - we're testing that the code properly handles an
    error condition. Division by zero is mathematically undefined, so our code
    should catch this and raise a clear error instead of crashing.
    
    We use pytest.raises to verify that the exception is thrown and that the
    error message is what we expect.
    
    Parameters:
    - a: Number attempting to divide
    - b: Zero (the invalid divisor)
    """
    # Act & Assert - we expect this to raise an exception
    with pytest.raises(ValueError, match="Division by zero is not allowed.") as exc_info:
        Operation.division(a, b)
    
    # Double-check the error message is exactly what we want
    assert "Division by zero is not allowed." in str(exc_info.value), \
        f"Expected specific error message, but got '{exc_info.value}'"

def test_division_with_zero_divisor():
    """
    Another test for division by zero, following a more explicit AAA pattern.
    
    This test does the same thing as the parameterized version above, but
    with a single case and clearer structure. Both approaches are valid.
    """
    # Arrange
    a = 10.0
    b = 0.0

    # Act & Assert - attempting division should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        Operation.division(a, b)
    
    # Verify the error message
    assert str(exc_info.value) == "Division by zero is not allowed."

# -----------------------------------------------------------------------------------
# Invalid Input Type Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize("calc_method, a, b, expected_exception", [
    (Operation.addition, '10', 5.0, TypeError),
    (Operation.subtraction, 10.0, '5', TypeError),
    (Operation.multiplication, '10', '5', TypeError),
    (Operation.division, 10.0, '5', TypeError),
])
def test_operations_invalid_input_types(calc_method, a, b, expected_exception):
    """
    Tests that operations raise TypeError when given non-numeric inputs.
    
    Our operations expect numbers, not strings. This test verifies that if someone
    accidentally passes a string, Python will raise a TypeError rather than giving
    a weird result or crashing unexpectedly.
    
    This is defensive programming - we want to catch bad inputs early with clear errors.
    
    Parameters:
    - calc_method: Which operation to test (addition, subtraction, etc.)
    - a: First input (one will be a string)
    - b: Second input (one will be a string)
    - expected_exception: Should be TypeError
    """
    # Act & Assert - passing strings should cause a TypeError
    with pytest.raises(expected_exception):
        calc_method(a, b)

# ------------------- Additional Test Cases -------------------

def test_addition_large_numbers():
    result = Operation.addition(1e9, 1e9)
    assert result == 2e9

def test_subtraction_negative_result():
    result = Operation.subtraction(5, 10)
    assert result == -5

def test_multiplication_negative_and_zero():
    result = Operation.multiplication(-7, 0)
    assert result == 0

def test_division_float_result():
    result = Operation.division(7, 2)
    assert result == 3.5

def test_division_negative_numerator():
    result = Operation.division(-8, 2)
    assert result == -4
