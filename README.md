# 🧮 Python Calculator & Web API Assignment

## Overview

This project is a modular Python calculator with a command-line REPL, arithmetic operations, and robust unit tests. It demonstrates best practices in Python packaging, testing, and automation.

**Features:**
- Addition, subtraction, multiplication, division (with error handling)
- Interactive REPL (command-line calculator)
- Calculation history and help commands
- Modular code structure
- Extensive unit tests

---

## Project Structure & Method Details

### app/operation/

**Operation class:**  
Implements core arithmetic functions as static methods:
- `addition(a, b)`: Returns the sum of `a` and `b`.
- `subtraction(a, b)`: Returns the difference of `a` and `b`.
- `multiplication(a, b)`: Returns the product of `a` and `b`.
- `division(a, b)`: Returns the quotient of `a` divided by `b`. Raises an error if `b` is zero.

These methods are used by calculation classes to perform actual math.

---

### app/calculation/

**Calculation (base class):**  
Defines the interface for all calculation types.  
- Stores operands `a` and `b`.
- Has an abstract `execute()` method to perform the calculation.

**AddCalculation, SubtractCalculation, MultiplyCalculation, DivideCalculation:**  
Each subclass implements `execute()` using the corresponding method from `Operation`.

**CalculationFactory:**  
- Registers calculation types and maps operation names to classes.
- `create_calculation(type, a, b)`: Returns an instance of the correct calculation class for the requested operation.

---

### app/calculator/

**REPL Logic:**  
- Reads user input in a loop.
- Parses commands and arguments.
- Uses `CalculationFactory` to create calculation objects.
- Calls `execute()` on calculation objects and displays results.
- Maintains a history list of calculation results.
- Handles special commands: `help`, `history`, `exit`.
- Provides error messages for invalid input, unsupported operations, and division by zero.

---

### main.py

- Entry point for the program.
- Starts the calculator REPL.

---

### tests/

- Contains unit tests for all modules.
- Tests cover correct results, error handling, and input validation.

---

## Demo Video

https://drive.google.com/file/d/1Iyrw100iOGPkZxIqCRy0oVBkigRZYfhP/view?usp=sharing
---

## Useful Commands

| Action                | Command                                  |
|-----------------------|------------------------------------------|
| Create venv           | `python3 -m venv venv`                   |
| Activate venv         | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install requirements  | `pip install -r requirements.txt`        |
| Run calculator        | `python main.py`                         |
| Run tests             | `pytest`                                 |
| Add & push changes    | `git add . && git commit -m "msg" && git push` |

---

## Notes

- Use Python 3.10+ and virtual environments.
- Docker setup is optional.
- See test files for example usage and edge cases.
