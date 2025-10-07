# Author: Varun Sabbineni 10/6/2025
# Calculation Model

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:
    """
    Represents a single calculation with all its details.

    This class stores everything about a calculation - what operation was performed,
    what numbers were used, what the result was, and when it happened. It handles
    performing the calculation, saving it to a format we can store, and loading it
    back when needed.
    
    We use a dataclass because it automatically handles a lot of the boilerplate code
    like __init__, making the class cleaner and easier to work with.
    """

    # Required fields that must be provided when creating a Calculation
    operation: str          # Name of the operation (like "Addition" or "Division")
    operand1: Decimal       # First number in the calculation
    operand2: Decimal       # Second number in the calculation

    # Fields that get set automatically
    result: Decimal = field(init=False)  # Calculated automatically after creation
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)  # Records when the calculation happened

    def __post_init__(self):
        """
        Runs automatically right after the Calculation object is created.

        This method calculates the result immediately after we set up the operation
        and operands, so every Calculation always has its result ready.
        """
        # Validate operand types before calculation
        if not isinstance(self.operand1, Decimal) or not isinstance(self.operand2, Decimal):
            raise OperationError("Operands must be Decimal instances")
        self.result = self.calculate()

    def calculate(self) -> Decimal:
        """
        Performs the actual calculation based on the operation type.

        Instead of a big if/elif chain, we use a dictionary that maps operation names
        to their corresponding functions (lambda functions in this case). This makes
        it easy to add new operations and keeps the code cleaner.

        Returns:
            Decimal: The calculated result

        Raises:
            OperationError: If the operation isn't recognized or something goes wrong
        """
        # Dictionary mapping operation names to their functions
        operations = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._raise_div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: (
                Decimal(pow(float(x), 1 / float(y))) 
                if x >= 0 and y != 0 
                else self._raise_invalid_root(x, y)
            )
        }

        # Look up the operation function by name
        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")

        try:
            # Execute the operation with our two operands
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            # Catch any math errors and wrap them in our custom exception
            raise OperationError(f"Calculation failed: {str(e)}")

    @staticmethod
    def _raise_div_zero():  # pragma: no cover
        """
        Helper method that raises an error for division by zero.

        We use a separate method for this so we can handle it cleanly in the
        lambda function above. It's a static method because it doesn't need
        access to any instance data.
        """
        raise OperationError("Division by zero is not allowed")

    @staticmethod
    def _raise_neg_power():  # pragma: no cover
        """
        Helper method that raises an error for negative exponents.

        Negative exponents would result in decimal/fractional results that might
        not be what users expect, so we don't support them in this calculator.
        """
        raise OperationError("Negative exponents are not supported")

    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal):  # pragma: no cover
        """
        Helper method that raises appropriate errors for invalid root operations.

        Root operations have special requirements - you can't take a root of degree
        zero, and you can't take a root of a negative number (at least not with
        real numbers). This method figures out which specific error to raise.

        Args:
            x: The number we're taking the root of
            y: The degree of the root (like 2 for square root)
        """
        if y == 0:
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Calculation into a dictionary for easy storage.

        This method transforms all the calculation data into a simple dictionary
        that can be saved to a file (like JSON or CSV). We convert Decimals to
        strings and timestamps to ISO format so everything is serializable.

        Returns:
            Dict: Dictionary with all calculation data in a storable format
        """
        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """
        Creates a Calculation object from a dictionary.

        This is the reverse of to_dict() - it takes saved data and reconstructs
        a Calculation object from it. We validate that all required fields are
        present and that the saved result matches what we calculate.

        Args:
            data: Dictionary containing the saved calculation data

        Returns:
            Calculation: A new Calculation object with the loaded data

        Raises:
            OperationError: If the data is missing fields or incorrectly formatted
        """
        try:
            # Create a new Calculation with the saved operands
            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2'])
            )

            # Restore the original timestamp from when it was saved
            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            # Double-check that our calculated result matches the saved result
            # This helps catch data corruption or version issues
            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                )  # pragma: no cover

            return calc

        except (KeyError, InvalidOperation, ValueError) as e:
            # If anything goes wrong, wrap the error in our custom exception
            raise OperationError(f"Invalid calculation data: {str(e)}")

    def __str__(self) -> str:
        """
        Creates a readable string representation of the calculation.

        This is what gets printed when you use print() or str() on a Calculation.
        It shows the operation and result in a clear, user-friendly format.

        Returns:
            str: Human-readable calculation string like "Addition(5, 3) = 8"
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"

    def __repr__(self) -> str:
        """
        Creates a detailed string representation for debugging.

        This shows all the internal details of the Calculation in a format that
        could theoretically be used to recreate the object. It's mainly useful
        when debugging to see exactly what values are stored.

        Returns:
            str: Detailed string showing all attributes
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Checks if two Calculations are equal.

        Two calculations are considered equal if they have the same operation,
        operands, and result. The timestamp doesn't matter for equality - we only
        care about the mathematical content.

        Args:
            other: Another object to compare with

        Returns:
            bool: True if the calculations are mathematically identical
        """
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )

    def format_result(self, precision: int = 10) -> str:
        """
        Formats the result with a specific number of decimal places.

        This method cleans up the result by limiting decimal places and removing
        unnecessary trailing zeros. It makes results look nicer when displaying
        them to users.

        Args:
            precision: How many decimal places to show (default 10)

        Returns:
            str: Nicely formatted result string
        """
        try:
            # Normalize removes trailing zeros, quantize sets precision
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation:  # pragma: no cover
            # If formatting fails for some reason, just return the raw result
            return str(self.result)
