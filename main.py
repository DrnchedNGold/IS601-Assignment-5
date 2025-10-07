"""
Advanced Calculator Application

A comprehensive calculator demonstrating professional Python programming practices.

Features:
- Basic arithmetic (add, subtract, multiply, divide)
- Advanced operations (power, root)
- Calculation history with save/load
- Undo/redo functionality
- Input validation and error handling
- Logging and configuration management

Design Patterns:
- Strategy: Swappable operations
- Observer: Auto-save and logging
- Factory: Creates operations dynamically
- Memento: Undo/redo state management

Code Organization:
- calculator.py: Main calculator logic
- calculator_repl.py: Command-line interface
- operations.py: Arithmetic operations
- calculation.py: Individual calculation objects
- history.py: Observers for calculations
- exceptions.py: Custom error types
- input_validators.py: Input validation
- calculator_config.py: Settings and configuration
- calculator_memento.py: State snapshots

Version: 1.0
"""

from app.calculator_repl import calculator_repl


if __name__ == "__main__":
    # Launch the interactive calculator interface
    calculator_repl()