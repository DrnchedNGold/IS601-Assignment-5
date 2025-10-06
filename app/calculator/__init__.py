# Author: Varun Sabbineni 9/30/2025
"""
Calculator module that handles user input and performs mathematical operations.
Supports basic arithmetic operations with enhanced features including command history,
help documentation, and calculation tracking.

This implementation showcases two fundamental Python programming approaches:
- LBYL (Look Before You Leap): Validate data before processing
- EAFP (Easier to Ask Forgiveness than Permission): Try operations and handle failures

"""

import sys
import readline  # Provides input history and line editing capabilities
from typing import List
from app.calculation import Calculation, CalculationFactory


def display_help() -> None:
    """
    Prints comprehensive usage instructions and available calculator operations.
    """
    help_message = """
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
    print(help_message)


def display_history(history: List[Calculation]) -> None:
    """
    Outputs the complete history of calculations from the current session.

    Parameters:
        history (List[Calculation]): Collection of Calculation objects from previous operations.
    """
    if not history:
        print("No calculations performed yet.")
    else:
        print("Calculation History:")
        for idx, calculation in enumerate(history, start=1):
            print(f"{idx}. {calculation}")


def calculator() -> None:
    """
    Main calculator function implementing a REPL (Read-Eval-Print Loop) interface.
    Handles arithmetic operations (add, subtract, multiply, divide) using Calculation classes.

    Demonstrates both LBYL and EAFPs for better error handling.
    """
    # Create an empty list to store the history of all calculations
    history: List[Calculation] = []

    # Display startup message to user
    print("Welcome to the Professional Calculator REPL!")
    print("Type 'help' for instructions or 'exit' to quit.\n")

    # Main loop that continues until user chooses to exit
    while True:
        try:
            # Get user input and remove leading/trailing whitespace
            user_input: str = input(">> ").strip()

            # LBYL (Look Before You Leap)
            # -----------------------------------
            # We check if the input is empty before processing it.
            # This preventive approach avoids unnecessary work on blank input.
            if not user_input:
                # Skip to next iteration if input is empty
                continue # pragma: no cover

            # Convert input to lowercase for command comparison
            command = user_input.lower()

            # LBYL: We verify if the input matches special commands before proceeding.
            if command == "help":
                display_help()
                continue
            elif command == "history":
                display_history(history)
                continue
            elif command == "exit":
                print("Exiting calculator. Goodbye!\n")
                sys.exit(0)  # Terminate the program cleanly

            # EAFP (Easier to Ask Forgiveness than Permission):
            # -----------------------------------
            # Rather than validating the input format beforehand (complex and tedious),
            # we try to parse it directly and catch any exceptions that occur.
            try:
                # Try to split input into three components: operation and two numbers
                operation, num1_str, num2_str = user_input.split()
                # Try converting the string numbers into float values
                num1: float = float(num1_str)
                num2: float = float(num2_str)
            except ValueError:
                # If parsing fails (wrong format or non-numeric input), catch the error.
                # EAFP approach: we attempted the operation and now handle the failure.
                print("Invalid input. Please follow the format: <operation> <num1> <num2>")
                print("Type 'help' for more information.\n")
                continue  # Return to start of loop for new input

            # Try creating a Calculation object via the factory method
            try:
                calculation = CalculationFactory.create_calculation(operation, num1, num2)
            except ValueError as ve:
                # Handle case where operation type is not supported
                print(ve)
                print("Type 'help' to see the list of supported operations.\n")
                continue  # Return to start of loop for new input

            # Try executing the calculation
            try:
                result = calculation.execute()
            except ZeroDivisionError:
                # Catch division by zero errors specifically
                print("Cannot divide by zero.")
                print("Please enter a non-zero divisor.\n")
                continue  # Return to start of loop for new input
            except Exception as e:
                # Catch any other unexpected exceptions
                print(f"An error occurred during calculation: {e}")
                print("Please try again.\n")
                continue  # Return to start of loop for new input

            # Format and display the calculation result
            result_str: str = f"{calculation}"
            print(f"Result: {result_str}\n")

            # Store the calculation in history
            history.append(calculation)

        except KeyboardInterrupt:
            # EAFP: Handle Ctrl+C without checking for it beforehand.
            # We respond to the interrupt exception when it happens.
            print("\nKeyboard interrupt detected. Exiting calculator. Goodbye!")
            sys.exit(0)
        except EOFError:
            # EAFP: Handle end-of-file (Ctrl+D) similarly.
            print("\nEOF detected. Exiting calculator. Goodbye!")
            sys.exit(0)


# Execute calculator if this script is run directly
if __name__ == "__main__":
    calculator() # pragma: no cover