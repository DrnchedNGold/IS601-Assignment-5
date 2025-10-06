# Author: Varun Sabbineni 9/30/2025
# tests/test_calculator.py

"""
This test file contains unit tests for the calculator REPL functionality.
Tests follow the Arrange-Act-Assert (AAA) pattern to keep them organized and readable.
"""

import pytest
from io import StringIO

# Import the functions we need to test
from app.calculator import display_help, display_history, calculator

def test_display_help(capsys):
    """
    Tests that the help command displays the correct information.

    AAA Pattern breakdown:
    - Arrange: Nothing to set up since display_help doesn't need parameters
    - Act: Call the function
    - Assert: Check that the output matches what we expect
    """
    # Arrange
    # No setup needed - display_help takes no arguments

    # Act
    display_help()

    # Assert
    # capsys captures anything printed to the console
    captured = capsys.readouterr()
    expected_output = """
Calculator REPL Help
--------------------
Usage:
    <operation> <number1> <number2>
    - Perform a calculation with the specified operation and two numbers.
    - Supported operations:
        add       : Adds two numbers.
        subtract  : Subtracts the second number from the first.
        multiply  : Multiplies two numbers.
        divide    : Divides the first number by the second.

Special Commands:
    help      : Display this help message.
    history   : Show the history of calculations.
    exit      : Exit the calculator.

Examples:
    add 10 5
    subtract 15.5 3.2
    multiply 7 8
    divide 20 4
"""
    # Strip whitespace to avoid issues with spacing differences
    assert captured.out.strip() == expected_output.strip()

def test_display_history_empty(capsys):
    """
    Tests that display_history shows the right message when no calculations exist.

    AAA Pattern:
    - Arrange: Create an empty history list
    - Act: Call display_history with that empty list
    - Assert: Verify it tells the user there's no history
    """
    # Arrange
    history = []

    # Act
    display_history(history)

    # Assert
    captured = capsys.readouterr()
    assert captured.out.strip() == "No calculations performed yet."

def test_display_history_with_entries(capsys):
    """
    Tests that display_history correctly shows multiple calculation entries.

    AAA Pattern:
    - Arrange: Create a history list with sample calculations
    - Act: Call display_history with the populated list
    - Assert: Verify each entry is displayed with proper numbering
    """
    # Arrange
    history = [
        "AddCalculation: 10.0 Add 5.0 = 15.0",
        "SubtractCalculation: 20.0 Subtract 3.0 = 17.0",
        "MultiplyCalculation: 7.0 Multiply 8.0 = 56.0",
        "DivideCalculation: 20.0 Divide 4.0 = 5.0"
    ]

    # Act
    display_history(history)

    # Assert
    captured = capsys.readouterr()
    expected_output = """Calculation History:
1. AddCalculation: 10.0 Add 5.0 = 15.0
2. SubtractCalculation: 20.0 Subtract 3.0 = 17.0
3. MultiplyCalculation: 7.0 Multiply 8.0 = 56.0
4. DivideCalculation: 20.0 Divide 4.0 = 5.0"""
    assert captured.out.strip() == expected_output.strip()

def test_calculator_exit(monkeypatch, capsys):
    """
    Tests that typing 'exit' properly closes the calculator.

    AAA Pattern:
    - Arrange: Set up input to simulate user typing 'exit'
    - Act: Run the calculator
    - Assert: Verify it exits cleanly with exit code 0
    """
    # Arrange
    user_input = 'exit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    # We expect the calculator to call sys.exit(), so we catch that with pytest.raises
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Exiting calculator. Goodbye!" in captured.out
    assert exc_info.type == SystemExit
    assert exc_info.value.code == 0  # 0 means clean exit, no errors

def test_calculator_help_command(monkeypatch, capsys):
    """
    Tests that the 'help' command displays instructions and then exits properly.

    AAA Pattern:
    - Arrange: Simulate typing 'help' then 'exit'
    - Act: Run the calculator
    - Assert: Check that help text appears before exit message
    """
    # Arrange
    user_input = 'help\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Calculator REPL Help" in captured.out
    assert "Exiting calculator. Goodbye!" in captured.out

def test_calculator_invalid_input(monkeypatch, capsys):
    """
    Tests that the calculator handles various types of invalid input gracefully.

    AAA Pattern:
    - Arrange: Set up several invalid inputs followed by exit
    - Act: Run the calculator
    - Assert: Verify error messages are shown for each invalid input
    """
    # Arrange
    user_input = 'invalid input\nadd 5\nsubtract\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Invalid input. Please follow the format: <operation> <num1> <num2>" in captured.out
    assert "Type 'help' for more information." in captured.out

def test_calculator_addition(monkeypatch, capsys):
    """
    Tests that addition calculations work correctly.

    AAA Pattern:
    - Arrange: Simulate 'add 10 5' command
    - Act: Run the calculator
    - Assert: Verify the result shows 15.0
    """
    # Arrange
    user_input = 'add 10 5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Result: AddCalculation: 10.0 Add 5.0 = 15.0" in captured.out

def test_calculator_subtraction(monkeypatch, capsys):
    """
    Tests that subtraction calculations work correctly.

    AAA Pattern:
    - Arrange: Simulate 'subtract 20 5' command
    - Act: Run the calculator
    - Assert: Verify the result shows 15.0
    """
    # Arrange
    user_input = 'subtract 20 5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Result: SubtractCalculation: 20.0 Subtract 5.0 = 15.0" in captured.out

def test_calculator_multiplication(monkeypatch, capsys):
    """
    Tests that multiplication calculations work correctly.

    AAA Pattern:
    - Arrange: Simulate 'multiply 7 8' command
    - Act: Run the calculator
    - Assert: Verify the result shows 56.0
    """
    # Arrange
    user_input = 'multiply 7 8\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Result: MultiplyCalculation: 7.0 Multiply 8.0 = 56.0" in captured.out

def test_calculator_division(monkeypatch, capsys):
    """
    Tests that division calculations work correctly.

    AAA Pattern:
    - Arrange: Simulate 'divide 20 4' command
    - Act: Run the calculator
    - Assert: Verify the result shows 5.0
    """
    # Arrange
    user_input = 'divide 20 4\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Result: DivideCalculation: 20.0 Divide 4.0 = 5.0" in captured.out

def test_calculator_division_by_zero(monkeypatch, capsys):
    """
    Tests that dividing by zero is caught and handled properly.

    AAA Pattern:
    - Arrange: Simulate 'divide 10 0' command
    - Act: Run the calculator
    - Assert: Verify an error message appears instead of crashing
    """
    # Arrange
    user_input = 'divide 10 0\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Cannot divide by zero." in captured.out

def test_calculator_history(monkeypatch, capsys):
    """
    Tests that the calculator remembers and displays calculation history.

    AAA Pattern:
    - Arrange: Simulate doing two calculations, then asking for history
    - Act: Run the calculator
    - Assert: Verify both calculations appear in the history output
    """
    # Arrange
    user_input = 'add 10 5\nsubtract 20 3\nhistory\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Result: AddCalculation: 10.0 Add 5.0 = 15.0" in captured.out
    assert "Result: SubtractCalculation: 20.0 Subtract 3.0 = 17.0" in captured.out
    assert "Calculation History:" in captured.out
    assert "1. AddCalculation: 10.0 Add 5.0 = 15.0" in captured.out
    assert "2. SubtractCalculation: 20.0 Subtract 3.0 = 17.0" in captured.out

def test_calculator_invalid_number_input(monkeypatch, capsys):
    """
    Tests that non-numeric inputs for numbers are handled gracefully.

    AAA Pattern:
    - Arrange: Simulate 'add ten five' (words instead of numbers)
    - Act: Run the calculator
    - Assert: Verify an appropriate error message is shown
    """
    # Arrange
    user_input = 'add ten five\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    # The error message might vary depending on how the code handles it
    assert "Invalid input. Please ensure numbers are valid." in captured.out or \
           "could not convert string to float: 'ten'" in captured.out or \
           "Invalid input. Please follow the format: <operation> <num1> <num2>" in captured.out

def test_calculator_unsupported_operation(monkeypatch, capsys):
    """
    Tests that requesting an operation that doesn't exist is handled properly.

    AAA Pattern:
    - Arrange: Simulate 'modulus 2 3' (an operation we don't support)
    - Act: Run the calculator
    - Assert: Verify the error message tells the user it's unsupported
    """
    # Arrange
    user_input = 'modulus 2 3\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Unsupported calculation type: 'modulus'." in captured.out
    assert "Type 'help' to see the list of supported operations." in captured.out

def test_calculator_keyboard_interrupt(monkeypatch, capsys):
    """
    Tests that pressing Ctrl+C exits the calculator gracefully.

    AAA Pattern:
    - Arrange: Mock the input function to raise KeyboardInterrupt
    - Act: Run the calculator
    - Assert: Verify it exits cleanly with an appropriate message
    """
    # Arrange
    def mock_input(prompt):
        raise KeyboardInterrupt()
    monkeypatch.setattr('builtins.input', mock_input)

    # Act
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "\nKeyboard interrupt detected. Exiting calculator. Goodbye!" in captured.out
    assert exc_info.value.code == 0

def test_calculator_eof_error(monkeypatch, capsys):
    """
    Tests that pressing Ctrl+D (EOF) exits the calculator gracefully.

    AAA Pattern:
    - Arrange: Mock the input function to raise EOFError
    - Act: Run the calculator
    - Assert: Verify it exits cleanly with an appropriate message
    """
    # Arrange
    def mock_input(prompt):
        raise EOFError()
    monkeypatch.setattr('builtins.input', mock_input)

    # Act
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "\nEOF detected. Exiting calculator. Goodbye!" in captured.out
    assert exc_info.value.code == 0

def test_calculator_unexpected_exception(monkeypatch, capsys):
    """
    Tests that unexpected errors during calculation are caught and handled.

    AAA Pattern:
    - Arrange: Create a mock calculation that raises an exception
    - Act: Run the calculator with this mock
    - Assert: Verify the error is caught and a helpful message is shown
    """
    # Arrange
    # Create a fake calculation class that will throw an error
    class MockCalculation:
        def execute(self):
            raise Exception("Mock exception during execution")
        def __str__(self):
            return "MockCalculation"

    # Replace the factory's create method with one that returns our mock
    def mock_create_calculation(operation, a, b):
        return MockCalculation()

    monkeypatch.setattr('app.calculation.CalculationFactory.create_calculation', mock_create_calculation)
    user_input = 'add 10 5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "An error occurred during calculation: Mock exception during execution" in captured.out
    assert "Please try again." in captured.out

# ------------------- Additional Test Cases -------------------

def test_calculator_multiply_by_zero(monkeypatch, capsys):
    user_input = 'multiply 0 12345\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Result: MultiplyCalculation: 0.0 Multiply 12345.0 = 0.0" in captured.out

def test_calculator_add_negative_numbers(monkeypatch, capsys):
    user_input = 'add -10 -5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Result: AddCalculation: -10.0 Add -5.0 = -15.0" in captured.out

def test_calculator_divide_floats(monkeypatch, capsys):
    user_input = 'divide 7.5 2.5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Result: DivideCalculation: 7.5 Divide 2.5 = 3.0" in captured.out

def test_calculator_large_numbers(monkeypatch, capsys):
    user_input = 'add 1000000 1000000\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Result: AddCalculation: 1000000.0 Add 1000000.0 = 2000000.0" in captured.out

def test_calculator_multiple_operations(monkeypatch, capsys):
    user_input = 'add 1 2\nmultiply 3 4\nsubtract 10 5\ndivide 20 4\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Result: AddCalculation: 1.0 Add 2.0 = 3.0" in captured.out
    assert "Result: MultiplyCalculation: 3.0 Multiply 4.0 = 12.0" in captured.out
    assert "Result: SubtractCalculation: 10.0 Subtract 5.0 = 5.0" in captured.out
    assert "Result: DivideCalculation: 20.0 Divide 4.0 = 5.0" in captured.out
