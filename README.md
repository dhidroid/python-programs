
# Dhidroid [https://github.com/dhidroid] | Abstract Fruit Inventory System

A Python object-oriented programming project demonstrating abstract
base classes, inheritance, polymorphism, encapsulation, validation,
and maintainable application design.

## Overview

The Abstract Fruit Inventory System evolves a basic fruit-class
example into an extensible Python application.

Instead of relying on ordinary methods containing `pass`, the
implementation uses Python's `abc` module to enforce a shared
contract for all concrete fruit classes.

The inventory manages different fruit types through one common
interface, avoiding fruit-specific conditional logic.

## Learning Objectives

- Understand abstract base classes and abstract properties.
- Implement inheritance and runtime polymorphism.
- Encapsulate state and validate application inputs.
- Use `Decimal` for monetary calculations.
- Design custom exceptions.
- Apply type hints and meaningful docstrings.
- Write automated tests with pytest.
- Follow the Open/Closed Principle when extending functionality.

## Features

- Abstract `Fruit` base class.
- Concrete `Apple`, `Banana`, and `Orange` classes.
- Validated fruit prices.
- Consistent fruit detail display.
- Inventory management.
- Case-insensitive fruit search.
- Average price calculation.
- Custom exceptions for invalid prices and empty inventories.
- Automated unit tests.

## Requirements

- Python 3.10 or later.
- pip.
- pytest for running the test suite.

## Project Structure

```text
python-programs/
├── absract.py
├── README.md
├── requirements.txt
└── tests/
    └── test_absract.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/obusakthi539/python-programs.git
cd python-programs
```

Create and activate a virtual environment.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python absract.py
```

The application displays each fruit's name, color, price per
kilogram, nutritional information, inventory count, and average
price.

The included prices are sample values for demonstration purposes.

## Example Usage

```python
from absract import Apple, Banana, FruitInventory

inventory = FruitInventory(
    [
        Apple(180),
        Banana(60),
    ]
)

inventory.display_inventory()

print(inventory.find_by_name("apple"))
print(inventory.average_price())
```

## Architecture

### 1. Abstract Base Class

`Fruit` inherits from `ABC` and defines the contract required
of every concrete fruit.

The abstract properties are:

- `name`
- `color`
- `nutrition`

Python prevents direct instantiation of the abstract class and
prevents instantiation of subclasses that leave abstract members
unimplemented.

### 2. Concrete Implementations

`Apple`, `Banana`, and `Orange` implement the abstract properties.

Each class provides its own fruit-specific information while
reusing the shared price validation and display behavior.

### 3. Encapsulation

The inventory stores fruit entries internally and exposes them
through a tuple. The price is stored in `_price_per_kg` and
validated when the fruit is initialized.

Python's underscore naming convention communicates intended
internal use; it does not provide strict private access control.

### 4. Polymorphism

`FruitInventory` calls the common interface rather than checking
the concrete class of each fruit.

A new fruit can be introduced without adding another branch to
the inventory display function.

### 5. Monetary Calculations

`Decimal` is used to represent prices and calculate the average.
This avoids many common binary floating-point representation
issues. Production billing systems may require additional rules
for currency precision and rounding.

## Adding a New Fruit

Implement the abstract properties in a new subclass.

```python
from absract import Fruit


class Mango(Fruit):
    @property
    def name(self) -> str:
        return "Mango"

    @property
    def color(self) -> str:
        return "Green"

    @property
    def nutrition(self) -> tuple[str, ...]:
        return ("Vitamin A", "Vitamin C")
```

Use the new class without modifying `FruitInventory`:

```python
from absract import FruitInventory

inventory = FruitInventory([Mango(120)])
inventory.display_inventory()
```

This demonstrates the Open/Closed Principle: the system is
open to extension without requiring changes to existing
inventory-display logic.

## Error Handling

The application defines the following exceptions:

| Exception | Purpose |
|---|---|
| `FruitError` | Base exception for inventory-related errors |
| `InvalidFruitPriceError` | Invalid, non-finite, or non-positive price |
| `EmptyInventoryError` | Average-price calculation on an empty inventory |

Invalid fruit objects passed to `FruitInventory.add_fruit`
raise `TypeError`.

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

The tests cover:

- Concrete fruit properties.
- Abstract-class instantiation.
- Incomplete subclass contracts.
- Price validation.
- Inventory operations.
- Search behavior.
- Average-price calculation.
- Empty-inventory handling.

## Design Discussion

1. Why is `ABC` with `@abstractmethod` more reliable than methods
   that simply contain `pass`?
2. How does polymorphism remove fruit-specific conditional logic?
3. How should the abstract contract be tested?
4. How does the design follow the Open/Closed Principle?
5. When would `typing.Protocol` be preferable to an abstract
   base class?

## Contribution Guidelines

1. Create a feature branch.
2. Implement the change with appropriate type hints.
3. Add tests for new behavior and relevant failure cases.
4. Run the full test suite.
5. Document design decisions in the pull request.
6. Submit a pull request with a clear summary and test results.

## Scope and Limitations

This is an educational OOP project, not a production inventory
or billing platform. It does not include persistent storage,
authentication, stock quantities, or a web API.

## License

No license is implied by this README. Add an explicit repository
license before permitting reuse under specific terms.

---

Maintained as a Python OOP learning contribution for the Dhidroid
engineering community.
