
# @author [ Dhidroid | dhineshkumar thirupathi ] @dhidroid  | Python OOP Engineering Challenge
# =========================================== 
#  @obusakthi539 - contributter

# Abstract Fruit Inventory System

# Demonstrates:
# - Abstract Base Classes and abstract properties
# - Inheritance and runtime polymorphism
# - Encapsulation and input validation
# - Decimal-based monetary calculations
# - Custom exceptions
# - Type hints and documentation
# - Inventory operations and search

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from typing import Iterable

# ============================================================ CUSTOM EXCEPTIONS ============================================================

class FruitError(Exception):
    # Base exception for fruit inventory operations. 
    pass


class InvalidFruitPriceError(FruitError, ValueError):
    # Raised when a fruit price is invalid.
    pass


class EmptyInventoryError(FruitError, ValueError):
    # Raised when an operation requires a non-empty inventory.
    pass


# ============================================================ABSTRACT BASE CLASS============================================================

class Fruit(ABC):
    # Abstract contract shared by all fruit types.

    # Concrete subclasses must implement the name, color,
    # and nutrition properties.

    def __init__(
        self,
        price_per_kg: Decimal | int | float | str,
    ) -> None:
        self._price_per_kg = self._validate_price(price_per_kg)

    @staticmethod
    def _validate_price(
        price: Decimal | int | float | str,
    ) -> Decimal:
        # Validate and normalize a fruit price.

        if isinstance(price, bool):
            raise InvalidFruitPriceError(
                "Boolean values are not valid prices."
            )

        if not isinstance(price, (Decimal, int, float, str)):
            raise InvalidFruitPriceError(
                "Price must be a Decimal, integer, float, or numeric string."
            )

        try:
            normalized = Decimal(str(price))
        except (InvalidOperation, ValueError):
            raise InvalidFruitPriceError(
                f"Invalid fruit price: {price!r}"
            ) from None

        if not normalized.is_finite():
            raise InvalidFruitPriceError(
                "Price must be a finite number."
            )

        if normalized <= Decimal("0"):
            raise InvalidFruitPriceError(
                "Price must be greater than zero."
            )

        return normalized

    @property
    @abstractmethod
    def name(self) -> str:
        # Return the fruit name.
        raise NotImplementedError

    @property
    @abstractmethod
    def color(self) -> str:
        # Return the fruit color.
        raise NotImplementedError

    @property
    @abstractmethod
    def nutrition(self) -> tuple[str, ...]:
        # Return nutritional information.
        raise NotImplementedError

    @property
    def price_per_kg(self) -> Decimal:
        # Return the validated price per kilogram.
        return self._price_per_kg

    def display_details(self) -> None:
        # Display the fruit's properties.

        print(f"Fruit      : {self.name}")
        print(f"Color      : {self.color}")
        print(f"Price / kg : ₹{self.price_per_kg:.2f}")
        print(f"Nutrition  : {', '.join(self.nutrition)}")

    def __str__(self) -> str:
        # Return a readable fruit description.

        return (
            f"{self.name} ({self.color}) - "
            f"₹{self.price_per_kg:.2f}/kg"
        )


# ============================================================  CONCRETE FRUIT CLASSES ============================================================


class Apple(Fruit):
    # Apple implementation of the Fruit contract.

    @property
    def name(self) -> str:
        return "Apple"

    @property
    def color(self) -> str:
        return "Red"

    @property
    def nutrition(self) -> tuple[str, ...]:
        return ("Fiber", "Vitamin C")


class Banana(Fruit):
    # Banana implementation of the Fruit contract.

    @property
    def name(self) -> str:
        return "Banana"

    @property
    def color(self) -> str:
        return "Yellow"

    @property
    def nutrition(self) -> tuple[str, ...]:
        return ("Potassium", "Vitamin B6")


class Orange(Fruit):
    # Orange implementation of the Fruit contract.

    @property
    def name(self) -> str:
        return "Orange"

    @property
    def color(self) -> str:
        return "Orange"

    @property
    def nutrition(self) -> tuple[str, ...]:
        return ("Vitamin C", "Fiber")


# ============================================================ INVENTORY SERVICE ============================================================

class FruitInventory:
    # 
    # Manage fruit objects through their common abstraction.

    # The inventory does not need fruit-specific display logic.
    # 

    def __init__(
        self,
        fruits: Iterable[Fruit] = (),
    ) -> None:
        self._fruits: list[Fruit] = []

        for fruit in fruits:
            self.add_fruit(fruit)

    def add_fruit(self, fruit: Fruit) -> None:
        # Add a concrete Fruit instance to the inventory.

        if not isinstance(fruit, Fruit):
            raise TypeError(
                "Inventory accepts only Fruit instances."
            )

        self._fruits.append(fruit)

    @property
    def fruits(self) -> tuple[Fruit, ...]:
        # Return a read-only view of inventory entries.

        return tuple(self._fruits)

    def display_inventory(self) -> None:
        # Display all inventory entries using polymorphism. 

        if not self._fruits:
            print("The fruit inventory is empty.")
            return

        print("\n" + "=" * 44)
        print("       DHIDROID FRUIT INVENTORY")
        print("=" * 44)

        for index, fruit in enumerate(self._fruits, start=1):
            print(f"\n[{index}]")
            fruit.display_details()
            print("-" * 44)

        print(f"Total entries      : {len(self._fruits)}")
        print(f"Average price / kg : ₹{self.average_price():.2f}")

    def average_price(self) -> Decimal:
        # Return the average price across inventory entries.

        if not self._fruits:
            raise EmptyInventoryError(
                "Cannot calculate an average for empty inventory."
            )

        total = sum(
            (fruit.price_per_kg for fruit in self._fruits),
            start=Decimal("0"),
        )

        return total / Decimal(len(self._fruits))

    def find_by_name(self, name: str) -> list[Fruit]:
        # Find fruits by name without case sensitivity.

        if not isinstance(name, str):
            raise TypeError("Fruit name must be a string.")

        normalized_name = name.strip().casefold()

        return [
            fruit
            for fruit in self._fruits
            if fruit.name.casefold() == normalized_name
        ]


# ============================================================ APPLICATION ENTRY POINT ============================================================

def main() -> None:
    # Run the sample fruit inventory application.

    inventory = FruitInventory(
        [
            Apple(180),
            Banana(60),
            Orange(100),
        ]
    )

    inventory.display_inventory()

    print("\nSearching for Apple:")

    for fruit in inventory.find_by_name("apple"):
        print(f"Found: {fruit}")


if __name__ == "__main__":
    main()
