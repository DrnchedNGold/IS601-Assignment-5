# Author: Varun Sabbineni 9/30/2025
# calculator_calculations.py

# -----------------------------------------------------------------------------------
# Import Statements
# -----------------------------------------------------------------------------------

# Importing ABC and abstractmethod to create abstract base classes.
# Abstract classes let us define a template that subclasses must follow, which helps
# ensure consistency across different types of calculations.
from abc import ABC, abstractmethod

# Importing the Operation class which contains our basic math operations.
# By keeping the arithmetic logic separate, we make the code more organized and easier
# to maintain. If we need to change how addition works, we only modify one place.
from app.operation import Operation

# -----------------------------------------------------------------------------------
# Abstract Base Class: Calculation
# -----------------------------------------------------------------------------------
class Calculation(ABC):
    """
    Calculation is an abstract base class that serves as a template for all math
    operations in our calculator. Every specific calculation type (addition, 
    subtraction, etc.) will inherit from this class.
    
    Why use an abstract base class?
    - Abstraction: We define what calculations need to do (have an execute method)
      without specifying exactly how each one works.
    - Polymorphism: All calculation types can be used interchangeably since they
      share the same interface, making our code more flexible.
    - Consistency: The abstract execute method guarantees that every calculation
      subclass will implement its own version of this method.
    """

    def __init__(self, a: float, b: float) -> None:
        """
        Sets up a new Calculation with two numbers to work with.
        
        Why have this initializer?
        - Every calculation needs two numbers to operate on, so we store them here.
        - Each Calculation object maintains its own values, which is a core principle
          of object-oriented design - objects hold their own data.

        Parameters:
        - a (float): First number in the calculation
        - b (float): Second number in the calculation
        """
        self.a: float = a  # Store the first number
        self.b: float = b  # Store the second number

    @abstractmethod
    def execute(self) -> float:
        """
        Abstract method that performs the actual calculation. Each subclass will
        provide its own implementation based on the specific operation.

        Why make this abstract?
        - Forces every subclass to implement execute, ensuring they all have this method.
        - Defines a required interface that all calculations must follow, making it
          easier to work with different calculation types in a uniform way.
        
        Returns:
        - float: The calculated result
        """
        pass  # Subclasses will provide the actual implementation # pragma: no cover

    def __str__(self) -> str:
        """
        Creates a readable string showing what the calculation does and its result.
        This makes it easier to understand what's happening when we print a calculation.

        Returns:
        - str: Human-readable description of the calculation
        """
        result = self.execute()  # Get the calculation result
        operation_name = self.__class__.__name__.replace('Calculation', '')  # Extract operation type
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"

    def __repr__(self) -> str:
        """
        Creates a technical representation showing the class name and values.
        This is particularly helpful when debugging because it shows exactly
        what the object contains in a consistent format.

        Returns:
        - str: Technical representation with class name and operand values
        """
        return f"{self.__class__.__name__}(a={self.a}, b={self.b})"

# -----------------------------------------------------------------------------------
# Factory Class: CalculationFactory
# -----------------------------------------------------------------------------------
class CalculationFactory:
    """
    CalculationFactory handles creating the right type of calculation based on
    user input. This is an example of the Factory design pattern, which separates
    the logic of creating objects from the objects themselves.

    Why use a factory?
    - Single Responsibility: The factory's only job is creating calculations, keeping
      the code organized and focused.
    - Flexibility: We can easily add new calculation types without changing existing
      code. Just register a new class and it's ready to use.
    - Open/Closed Principle: The code is open for extension (adding new types) but
      closed for modification (we don't need to change existing logic).
    """

    # Dictionary that maps calculation names (like "add") to their corresponding classes
    _calculations = {}

    @classmethod
    def register_calculation(cls, calculation_type: str):
        """
        Decorator that registers a calculation class with a specific name.
        This allows us to map string identifiers like "add" to the actual
        AddCalculation class.

        Parameters:
        - calculation_type (str): Short identifier for the calculation (e.g., 'add')
        
        Benefits of using a decorator:
        - Modularity: New calculations can be added just by decorating a new class.
        - Dynamic registration: We can add new operation types at runtime without
          hardcoding them into the factory.
        """
        def decorator(subclass):
            # Make it case-insensitive by converting to lowercase
            calculation_type_lower = calculation_type.lower()
            # Prevent duplicate registrations
            if calculation_type_lower in cls._calculations:
                raise ValueError(f"Calculation type '{calculation_type}' is already registered.")
            # Add this calculation to our registry
            cls._calculations[calculation_type_lower] = subclass
            return subclass  # Return the class so it can still be used normally
        return decorator

    @classmethod
    def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        """
        Factory method that creates the appropriate calculation object based on
        the type requested.

        Parameters:
        - calculation_type (str): Type of calculation ('add', 'subtract', 'multiply', 'divide')
        - a (float): First number
        - b (float): Second number
        
        Returns:
        - Calculation: An instance of the requested calculation type

        How this helps:
        - Centralized creation: All calculation objects are created here, making it
          easy to manage and modify the creation process.
        - Dynamic selection: We can choose which calculation to create at runtime
          based on user input.
        - Error handling: If someone requests an invalid type, we provide a helpful
          error message listing the valid options.
        """
        calculation_type_lower = calculation_type.lower()
        calculation_class = cls._calculations.get(calculation_type_lower)
        # If the type isn't registered, show available options
        if not calculation_class:
            available_types = ', '.join(cls._calculations.keys())
            raise ValueError(f"Unsupported calculation type: '{calculation_type}'. Available types: {available_types}")
        # Create and return the requested calculation with the given numbers
        return calculation_class(a, b)

# -----------------------------------------------------------------------------------
# Concrete Calculation Classes
# -----------------------------------------------------------------------------------

# These classes represent specific types of calculations. Each inherits from Calculation
# and implements the execute method to perform its particular operation.

@CalculationFactory.register_calculation('add')
class AddCalculation(Calculation):
    """
    Handles addition operations.
    
    Why separate classes for each operation?
    - Polymorphism: Each type can be used interchangeably through the execute method.
    - Modularity: Changes to one operation don't affect others.
    - Clear purpose: Each class has one specific job, making the code easier to
      understand and maintain.
    """

    def execute(self) -> float:
        # Use the addition method from Operation to calculate the sum
        return Operation.addition(self.a, self.b)


@CalculationFactory.register_calculation('subtract')
class SubtractCalculation(Calculation):
    """
    Handles subtraction operations.
    
    Keeping subtraction separate ensures changes to this operation won't
    accidentally affect other calculation types.
    """

    def execute(self) -> float:
        # Use the subtraction method from Operation to calculate the difference
        return Operation.subtraction(self.a, self.b)


@CalculationFactory.register_calculation('multiply')
class MultiplyCalculation(Calculation):
    """
    Handles multiplication operations.
    
    By encapsulating multiplication here, we maintain clear separation of concerns,
    making it straightforward to modify multiplication without touching other operations.
    """

    def execute(self) -> float:
        # Use the multiplication method from Operation to calculate the product
        return Operation.multiplication(self.a, self.b)


@CalculationFactory.register_calculation('divide')
class DivideCalculation(Calculation):
    """
    Handles division operations.
    
    Important: Division needs special handling for the case where someone tries
    to divide by zero, which would crash the program. We check for this before
    attempting the division.
    """

    def execute(self) -> float:
        # Check if we're trying to divide by zero before proceeding
        if self.b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        # Use the division method from Operation to calculate the quotient
        return Operation.division(self.a, self.b)

# @CalculationFactory.register_calculation('power')
# class PowerCalculation(Calculation):
#     """
#     Handles exponentiation operations.
    
#     This would allow raising one number to the power of another, expanding
#     the calculator's capabilities beyond basic arithmetic.
#     """

#     def execute(self) -> float:
#         # Use the power method from Operation to calculate the exponentiation
#         return Operation.power(self.a, self.b) # pragma: no cover