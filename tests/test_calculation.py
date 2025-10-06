# Author: Varun Sabbineni 9/30/2025
# tests/test_calculations.py

"""
Unit tests for the calculation classes and CalculationFactory.

This file tests all the calculation classes (AddCalculation, SubtractCalculation, etc.)
and the factory that creates them. We use mocking to isolate our tests and make sure
each component works correctly on its own.

Tests follow the AAA pattern and include both positive tests (things should work)
and negative tests (errors should be handled properly).
"""

import pytest
from unittest.mock import patch
from app.operation import Operation
from app.calculation import (
    CalculationFactory,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    Calculation
)


# -----------------------------------------------------------------------------------
# Tests for Individual Calculation Classes
# -----------------------------------------------------------------------------------

@patch.object(Operation, 'addition')
def test_add_calculation_execute_positive(mock_addition):
    """
    Tests that AddCalculation correctly calls the addition method and returns the result.
    
    We use mocking here to isolate the test - we're not testing whether addition works
    (that's tested in test_operations.py), we're testing whether AddCalculation properly
    calls the addition method with the right parameters.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 15.0
    mock_addition.return_value = expected_result  # Tell the mock what to return
    add_calc = AddCalculation(a, b)

    # Act
    result = add_calc.execute()

    # Assert
    mock_addition.assert_called_once_with(a, b)  # Verify addition was called correctly
    assert result == expected_result


@patch.object(Operation, 'addition')
def test_add_calculation_execute_negative(mock_addition):
    """
    Tests that AddCalculation properly handles errors from the addition method.
    
    This is a negative test - we're making sure that if something goes wrong in
    the underlying addition operation, the error gets passed along correctly
    rather than being hidden or causing unexpected behavior.
    """
    # Arrange
    a = 10.0
    b = 5.0
    mock_addition.side_effect = Exception("Addition error")  # Make the mock raise an error
    add_calc = AddCalculation(a, b)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        add_calc.execute()

    # Verify the error message matches what we expect
    assert str(exc_info.value) == "Addition error"


@patch.object(Operation, 'subtraction')
def test_subtract_calculation_execute_positive(mock_subtraction):
    """
    Tests that SubtractCalculation correctly calls the subtraction method.
    
    Similar to the addition test, we're verifying that the calculation class
    properly delegates to the operations class.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 5.0
    mock_subtraction.return_value = expected_result
    subtract_calc = SubtractCalculation(a, b)

    # Act
    result = subtract_calc.execute()

    # Assert
    mock_subtraction.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'subtraction')
def test_subtract_calculation_execute_negative(mock_subtraction):
    """
    Tests that SubtractCalculation properly propagates errors.
    """
    # Arrange
    a = 10.0
    b = 5.0
    mock_subtraction.side_effect = Exception("Subtraction error")
    subtract_calc = SubtractCalculation(a, b)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        subtract_calc.execute()

    assert str(exc_info.value) == "Subtraction error"


@patch.object(Operation, 'multiplication')
def test_multiply_calculation_execute_positive(mock_multiplication):
    """
    Tests that MultiplyCalculation correctly calls the multiplication method.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 50.0
    mock_multiplication.return_value = expected_result
    multiply_calc = MultiplyCalculation(a, b)

    # Act
    result = multiply_calc.execute()

    # Assert
    mock_multiplication.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'multiplication')
def test_multiply_calculation_execute_negative(mock_multiplication):
    """
    Tests that MultiplyCalculation properly propagates errors.
    """
    # Arrange
    a = 10.0
    b = 5.0
    mock_multiplication.side_effect = Exception("Multiplication error")
    multiply_calc = MultiplyCalculation(a, b)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        multiply_calc.execute()

    assert str(exc_info.value) == "Multiplication error"


@patch.object(Operation, 'division')
def test_divide_calculation_execute_positive(mock_division):
    """
    Tests that DivideCalculation correctly calls the division method.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 2.0
    mock_division.return_value = expected_result
    divide_calc = DivideCalculation(a, b)

    # Act
    result = divide_calc.execute()

    # Assert
    mock_division.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'division')
def test_divide_calculation_execute_negative(mock_division):
    """
    Tests that DivideCalculation properly propagates errors.
    """
    # Arrange
    a = 10.0
    b = 5.0
    mock_division.side_effect = Exception("Division error")
    divide_calc = DivideCalculation(a, b)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        divide_calc.execute()

    assert str(exc_info.value) == "Division error"


def test_divide_calculation_execute_division_by_zero():
    """
    Tests that dividing by zero raises the correct error.
    
    This test doesn't use mocking because we want to verify the actual division
    by zero handling. DivideCalculation should check for zero before calling
    the division method and raise a ZeroDivisionError with a clear message.
    """
    # Arrange
    a = 10.0
    b = 0.0
    divide_calc = DivideCalculation(a, b)

    # Act & Assert
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide_calc.execute()

    # Verify we get the expected error message
    assert str(exc_info.value) == "Cannot divide by zero."


# -----------------------------------------------------------------------------------
# Tests for CalculationFactory
# -----------------------------------------------------------------------------------

def test_factory_creates_add_calculation():
    """
    Tests that the factory creates an AddCalculation when asked for 'add'.
    
    The factory pattern allows us to create different calculation objects
    dynamically based on a string input. This test verifies that when we
    ask for 'add', we get back an AddCalculation instance with the right values.
    """
    # Arrange
    a = 10.0
    b = 5.0

    # Act
    calc = CalculationFactory.create_calculation('add', a, b)

    # Assert
    assert isinstance(calc, AddCalculation)  # Check it's the right type
    assert calc.a == a  # Verify it stored the first number
    assert calc.b == b  # Verify it stored the second number

def test_factory_creates_add_calculation_with_floats():
    """
    Tests that the factory creates an AddCalculation with float values.
    """
    a = 2.5
    b = 3.5
    calc = CalculationFactory.create_calculation('add', a, b)
    assert isinstance(calc, AddCalculation)
    assert calc.a == a
    assert calc.b == b

def test_multiply_calculation_execute_zero():
    """
    Tests that multiplying by zero returns zero.
    """
    multiply_calc = MultiplyCalculation(0.0, 12345.6)
    with patch.object(Operation, 'multiplication', return_value=0.0) as mock_multiplication:
        result = multiply_calc.execute()
        mock_multiplication.assert_called_once_with(0.0, 12345.6)
        assert result == 0.0

def test_divide_calculation_execute_negative():
    """
    Tests division by a negative number.
    """
    divide_calc = DivideCalculation(10.0, -2.0)
    with patch.object(Operation, 'division', return_value=-5.0) as mock_division:
        result = divide_calc.execute()
        mock_division.assert_called_once_with(10.0, -2.0)
        assert result == -5.0

    """
    Tests that the factory creates an AddCalculation when asked for 'add'.
    
    The factory pattern allows us to create different calculation objects
    dynamically based on a string input. This test verifies that when we
    ask for 'add', we get back an AddCalculation instance with the right values.
    """
    # Arrange
    a = 10.0
    b = 5.0

    # Act
    calc = CalculationFactory.create_calculation('add', a, b)

    # Assert
    assert isinstance(calc, AddCalculation)  # Check it's the right type
    assert calc.a == a  # Verify it stored the first number
    assert calc.b == b  # Verify it stored the second number


def test_factory_creates_subtract_calculation():
    """
    Tests that the factory creates a SubtractCalculation when asked for 'subtract'.
    """
    # Arrange
    a = 10.0
    b = 5.0

    # Act
    calc = CalculationFactory.create_calculation('subtract', a, b)

    # Assert
    assert isinstance(calc, SubtractCalculation)
    assert calc.a == a
    assert calc.b == b


def test_factory_creates_multiply_calculation():
    """
    Tests that the factory creates a MultiplyCalculation when asked for 'multiply'.
    """
    # Arrange
    a = 10.0
    b = 5.0

    # Act
    calc = CalculationFactory.create_calculation('multiply', a, b)

    # Assert
    assert isinstance(calc, MultiplyCalculation)
    assert calc.a == a
    assert calc.b == b


def test_factory_creates_divide_calculation():
    """
    Tests that the factory creates a DivideCalculation when asked for 'divide'.
    """
    # Arrange
    a = 10.0
    b = 5.0

    # Act
    calc = CalculationFactory.create_calculation('divide', a, b)

    # Assert
    assert isinstance(calc, DivideCalculation)
    assert calc.a == a
    assert calc.b == b


def test_factory_create_unsupported_calculation():
    """
    Tests that requesting an unsupported operation raises a clear error.
    
    If someone asks for a calculation type that doesn't exist (like 'modulus'),
    the factory should raise a ValueError with a helpful message listing the
    available options. This helps users understand what went wrong.
    """
    # Arrange
    a = 10.0
    b = 5.0
    unsupported_type = 'modulus'

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation(unsupported_type, a, b)

    # Verify the error message mentions the unsupported type
    assert f"Unsupported calculation type: '{unsupported_type}'" in str(exc_info.value)


def test_factory_register_calculation_duplicate():
    """
    Tests that trying to register a duplicate calculation type raises an error.
    
    The factory keeps track of which calculation types are registered. If someone
    tries to register the same type twice (like registering 'add' again), it should
    raise a ValueError to prevent confusion and bugs.
    """
    # Arrange & Act
    with pytest.raises(ValueError) as exc_info:
        @CalculationFactory.register_calculation('add')  # 'add' is already registered
        class AnotherAddCalculation(Calculation):
            """
            Attempting to register a duplicate - this should fail.
            """
            def execute(self) -> float:
                return Operation.addition(self.a, self.b)

    # Assert
    assert "Calculation type 'add' is already registered." in str(exc_info.value)


# -----------------------------------------------------------------------------------
# Tests for String Representations
# -----------------------------------------------------------------------------------

@patch.object(Operation, 'addition', return_value=15.0)
def test_calculation_str_representation_addition(mock_addition):
    """
    Tests that AddCalculation's string representation is formatted correctly.
    
    The __str__ method should create a human-readable string showing what the
    calculation is and what result it gives. This is useful for displaying
    results to users and for debugging.
    """
    # Arrange
    a = 10.0
    b = 5.0
    add_calc = AddCalculation(a, b)

    # Act
    calc_str = str(add_calc)

    # Assert
    # The string should show the class name, operands, and result
    expected_str = f"{add_calc.__class__.__name__}: {a} Add {b} = 15.0"
    assert calc_str == expected_str


@patch.object(Operation, 'subtraction', return_value=5.0)
def test_calculation_str_representation_subtraction(mock_subtraction):
    """
    Tests that SubtractCalculation's string representation is formatted correctly.
    """
    # Arrange
    a = 10.0
    b = 5.0
    subtract_calc = SubtractCalculation(a, b)

    # Act
    calc_str = str(subtract_calc)

    # Assert
    expected_str = f"{subtract_calc.__class__.__name__}: {a} Subtract {b} = 5.0"
    assert calc_str == expected_str


@patch.object(Operation, 'multiplication', return_value=50.0)
def test_calculation_str_representation_multiplication(mock_multiplication):
    """
    Tests that MultiplyCalculation's string representation is formatted correctly.
    """
    # Arrange
    a = 10.0
    b = 5.0
    multiply_calc = MultiplyCalculation(a, b)

    # Act
    calc_str = str(multiply_calc)

    # Assert
    expected_str = f"{multiply_calc.__class__.__name__}: {a} Multiply {b} = 50.0"
    assert calc_str == expected_str


@patch.object(Operation, 'division', return_value=2.0)
def test_calculation_str_representation_division(mock_division):
    """
    Tests that DivideCalculation's string representation is formatted correctly.
    """
    # Arrange
    a = 10.0
    b = 5.0
    divide_calc = DivideCalculation(a, b)

    # Act
    calc_str = str(divide_calc)

    # Assert
    expected_str = f"{divide_calc.__class__.__name__}: {a} Divide {b} = 2.0"
    assert calc_str == expected_str


def test_calculation_repr_representation_subtraction():
    """
    Tests that SubtractCalculation's repr is formatted correctly.
    
    The __repr__ method gives a more technical representation that shows exactly
    how to recreate the object. It's mainly used for debugging and should show
    the class name and the parameter values.
    """
    # Arrange
    a = 10.0
    b = 5.0
    subtract_calc = SubtractCalculation(a, b)

    # Act
    calc_repr = repr(subtract_calc)

    # Assert
    expected_repr = f"{SubtractCalculation.__name__}(a={a}, b={b})"
    assert calc_repr == expected_repr


def test_calculation_repr_representation_division():
    """
    Tests that DivideCalculation's repr is formatted correctly.
    """
    # Arrange
    a = 10.0
    b = 5.0
    divide_calc = DivideCalculation(a, b)

    # Act
    calc_repr = repr(divide_calc)

    # Assert
    expected_repr = f"{DivideCalculation.__name__}(a={a}, b={b})"
    assert calc_repr == expected_repr


# -----------------------------------------------------------------------------------
# Parameterized Tests
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize("calc_type, a, b, expected_result", [
    ('add', 10.0, 5.0, 15.0),
    ('subtract', 10.0, 5.0, 5.0),
    ('multiply', 10.0, 5.0, 50.0),
    ('divide', 10.0, 5.0, 2.0),
    # Additional cases
    ('add', -3.0, 7.0, 4.0),
    ('subtract', 5.5, 2.2, 3.3),
    ('multiply', 0.0, 100.0, 0.0),
    ('divide', -10.0, 2.0, -5.0),
    ('add', 1e6, 1e6, 2e6),
])
@patch.object(Operation, 'addition')
@patch.object(Operation, 'subtraction')
@patch.object(Operation, 'multiplication')
@patch.object(Operation, 'division')
def test_calculation_execute_parameterized(
    mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_type, a, b, expected_result
):
    """
    Parameterized test that verifies all calculation types work correctly.
    
    Instead of writing four separate tests that all do basically the same thing,
    we use parameterization to test all four calculation types with one test function.
    This reduces code duplication and makes it easier to add new calculation types.
    """
    # Arrange - set up the appropriate mock based on which calculation we're testing
    if calc_type == 'add':
        mock_addition.return_value = expected_result
    elif calc_type == 'subtract':
        mock_subtraction.return_value = expected_result
    elif calc_type == 'multiply':
        mock_multiplication.return_value = expected_result
    elif calc_type == 'divide':
        mock_division.return_value = expected_result

    # Act - create the calculation and execute it
    calc = CalculationFactory.create_calculation(calc_type, a, b)
    result = calc.execute()

    # Assert - verify the correct operation was called and the result is right
    if calc_type == 'add':
        mock_addition.assert_called_once_with(a, b)
    elif calc_type == 'subtract':
        mock_subtraction.assert_called_once_with(a, b)
    elif calc_type == 'multiply':
        mock_multiplication.assert_called_once_with(a, b)
    elif calc_type == 'divide':
        mock_division.assert_called_once_with(a, b)

    assert result == expected_result


@pytest.mark.parametrize("calc_type, a, b, expected_str", [
    ('add', 10.0, 5.0, "AddCalculation: 10.0 Add 5.0 = 15.0"),
    ('subtract', 10.0, 5.0, "SubtractCalculation: 10.0 Subtract 5.0 = 5.0"),
    ('multiply', 10.0, 5.0, "MultiplyCalculation: 10.0 Multiply 5.0 = 50.0"),
    ('divide', 10.0, 5.0, "DivideCalculation: 10.0 Divide 5.0 = 2.0"),
    # Additional cases
    ('add', -3.0, 7.0, "AddCalculation: -3.0 Add 7.0 = 15.0"),
    ('subtract', 5.5, 2.2, "SubtractCalculation: 5.5 Subtract 2.2 = 5.0"),
    ('multiply', 0.0, 100.0, "MultiplyCalculation: 0.0 Multiply 100.0 = 50.0"),
    ('divide', -10.0, 2.0, "DivideCalculation: -10.0 Divide 2.0 = 2.0"),
    ('add', 1e6, 1e6, "AddCalculation: 1000000.0 Add 1000000.0 = 15.0"),
])
@patch.object(Operation, 'addition', return_value=15.0)
@patch.object(Operation, 'subtraction', return_value=5.0)
@patch.object(Operation, 'multiplication', return_value=50.0)
@patch.object(Operation, 'division', return_value=2.0)
def test_calculation_str_parameterized(
    mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_type, a, b, expected_str
):
    """
    Parameterized test for string representations of all calculation types.
    
    Similar to the execute test, this verifies that all calculation types produce
    correctly formatted string representations without writing separate tests for each.
    """
    # Act - create the calculation and get its string representation
    calc = CalculationFactory.create_calculation(calc_type, a, b)
    calc_str = str(calc)

    # Assert - verify the string matches the expected format
    assert calc_str == expected_str
