# Author: Varun Sabbineni 9/30/2025
# operations.py

class Operation:
    """
    The Operation class groups arithmetic operations together using static methods.
    This approach organizes related functionality in one place, making the code more modular.
    
    Key design concepts:
    - Encapsulation: Related operations are grouped together for better organization
    - Abstraction: Users can call these methods without worrying about implementation details
    - Reusability: Static methods can be used throughout the program without creating instances
    
    Static methods are used because these operations don't need any instance-specific data.
    They work independently based only on the parameters passed to them, making them
    ideal for utility functions like basic arithmetic.
    """

    @staticmethod
    def addition(a: float, b: float) -> float:
        """
        Adds two numbers together and returns the sum.

        Parameters:
        - a (float): First number to add
        - b (float): Second number to add
        
        Returns:
        - float: Sum of a and b

        Example:
        >>> Operation.addition(5.0, 3.0)
        8.0

        Static methods work well here because addition doesn't depend on any object state,
        only on the input values provided.
        """
        return a + b  # Calculates and returns the sum of both numbers

    @staticmethod
    def subtraction(a: float, b: float) -> float:
        """
        Subtracts the second number from the first and returns the difference.

        Parameters:
        - a (float): Number to subtract from
        - b (float): Number to subtract
        
        Returns:
        - float: Difference between a and b

        Example:
        >>> Operation.subtraction(10.0, 4.0)
        6.0

        Each operation has its own method following the Single Responsibility Principle,
        where each function handles one specific task. This makes testing and maintenance
        easier since each operation is isolated.
        """
        return a - b  # Calculates and returns the difference between the numbers

    @staticmethod
    def multiplication(a: float, b: float) -> float:
        """
        Multiplies two numbers together and returns the product.

        Parameters:
        - a (float): First number to multiply
        - b (float): Second number to multiply
        
        Returns:
        - float: Product of a and b

        Example:
        >>> Operation.multiplication(2.0, 3.0)
        6.0

        Using static methods in utility classes like this provides straightforward access
        to functionality without the overhead of creating class instances.
        """
        return a * b  # Calculates and returns the product of both numbers

    @staticmethod
    def division(a: float, b: float) -> float:
        """
        Divides the first number by the second and returns the quotient.

        Parameters:
        - a (float): Dividend (number being divided)
        - b (float): Divisor (number dividing by)
        
        Returns:
        - float: Quotient of a divided by b

        Raises:
        - ValueError: When divisor b is zero, since division by zero is undefined

        Example:
        >>> Operation.division(10.0, 2.0)
        5.0
        >>> Operation.division(10.0, 0.0)
        Traceback (most recent call last):
            ...
        ValueError: Division by zero is not allowed.

        Error handling is critical for division. We check if b is zero before attempting
        the operation to prevent runtime errors. This is an example of defensive programming,
        where we anticipate potential issues and handle them explicitly rather than letting
        the program fail unexpectedly.
        """
        if b == 0:
            # Validates that the divisor isn't zero before proceeding with division
            raise ValueError("Division by zero is not allowed.")  # Prevents undefined mathematical operation
        return a / b  # Calculates and returns the quotient