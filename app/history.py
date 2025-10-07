# Author: Varun Sabbineni 10/6/2025
# History Management

from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


class HistoryObserver(ABC):
    """
    Abstract base class that defines what observers need to implement.

    This is the Observer pattern in action. Observers "watch" the calculator and
    get notified whenever something interesting happens (like a new calculation).
    Each observer can react differently to the same event.

    Any class that wants to observe the calculator must inherit from this and
    implement the update method. This ensures all observers have a consistent
    interface that the calculator can rely on.
    """

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """
        Gets called when a new calculation happens.

        This is the method that the calculator calls to notify the observer.
        Each observer implements this differently based on what it needs to do.

        Args:
            calculation: The calculation that just happened
        """
        pass  # pragma: no cover


class LoggingObserver(HistoryObserver):
    """
    Observer that writes calculation details to the log file.

    This observer's job is simple - whenever a calculation happens, log it.
    This creates an audit trail we can review later to see what calculations
    were performed and when.

    It's useful for debugging issues or understanding how the calculator is
    being used.
    """

    def update(self, calculation: Calculation) -> None:
        """
        Logs the calculation details to the log file.

        When the calculator notifies this observer about a new calculation,
        we write the operation, operands, and result to the log. This gives
        us a permanent record of everything the calculator does.

        Args:
            calculation: The calculation to log
        
        Raises:
            AttributeError: If calculation is None (shouldn't happen, but we check)
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        # Write a detailed log entry with all the calculation info
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """
    Observer that automatically saves history after each calculation.

    This observer implements the "auto-save" feature. Whenever a new calculation
    happens, if auto-save is enabled in the config, this observer triggers a
    save to the history file.

    This way users don't lose their work if something crashes - the history is
    constantly being saved in the background without them having to think about it.
    """

    def __init__(self, calculator: Any):
        """
        Sets up the observer with a reference to the calculator.

        We need to keep a reference to the calculator so we can call its
        save_history method when needed. We also validate that the calculator
        has the attributes we need to use.

        Args:
            calculator: The calculator instance we're observing
        
        Raises:
            TypeError: If the calculator doesn't have the methods/attributes we need
        """
        # Verify the calculator has what we need before proceeding
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """
        Saves the history if auto-save is enabled.

        When notified of a new calculation, we check if auto-save is turned on
        in the configuration. If it is, we tell the calculator to save its history.
        If auto-save is off, we don't do anything.

        Args:
            calculation: The calculation that was just performed
        
        Raises:
            AttributeError: If calculation is None
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        # Only save if auto-save is enabled in the config
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")