# Author: Varun Sabbineni 9/30/2025
# tests/conftest.py

# Importing pytest to use its testing features, particularly fixtures
import pytest
# Importing CalculationFactory which creates our calculation objects
from app.calculation import CalculationFactory
# Importing all the specific calculation classes we need to re-register
from app.calculation import (
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    
)

@pytest.fixture(autouse=True)
def reset_calculation_factory():
    """
    This fixture automatically runs before each test to ensure CalculationFactory
    starts with a clean slate. This prevents tests from interfering with each other.
    
    Why do we need this?
    - Tests should be independent: Each test should run the same way regardless of
      what other tests have done. Without this reset, one test could register a
      calculation that affects another test's results.
    - Fresh state: By clearing and re-registering calculations before each test,
      we guarantee that every test starts with the exact same setup.
    - autouse=True: This means pytest will automatically call this fixture before
      every test without us having to explicitly include it in each test function.
    """
    # Remove any calculations that might have been registered previously
    CalculationFactory._calculations.clear()

    # Set up the standard calculations again so they're available for testing
    # We manually re-register each one because clearing removed them all
    CalculationFactory.register_calculation('add')(AddCalculation)
    CalculationFactory.register_calculation('subtract')(SubtractCalculation)
    CalculationFactory.register_calculation('multiply')(MultiplyCalculation)
    CalculationFactory.register_calculation('divide')(DivideCalculation)