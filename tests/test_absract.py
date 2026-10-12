
from decimal import Decimal

import pytest

from absract import (
    Apple,
    Banana,
    EmptyInventoryError,
    Fruit,
    FruitInventory,
    InvalidFruitPriceError,
    Orange,
)


def test_apple_properties():
    apple = Apple(180)

    assert apple.name == "Apple"
    assert apple.color == "Red"
    assert apple.price_per_kg == Decimal("180")
    assert apple.nutrition == ("Fiber", "Vitamin C")


def test_banana_properties():
    banana = Banana(60)

    assert banana.name == "Banana"
    assert banana.color == "Yellow"
    assert banana.price_per_kg == Decimal("60")


def test_orange_properties():
    orange = Orange(100)

    assert orange.name == "Orange"
    assert orange.color == "Orange"
    assert orange.price_per_kg == Decimal("100")


def test_abstract_fruit_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Fruit(100)


def test_incomplete_subclass_cannot_be_instantiated():
    class IncompleteFruit(Fruit):
        @property
        def name(self) -> str:
            return "Incomplete"

    with pytest.raises(TypeError):
        IncompleteFruit(100)


@pytest.mark.parametrize(
    "invalid_price",
    [
        0,
        -10,
        Decimal("0"),
        Decimal("-1"),
        float("nan"),
        float("inf"),
        "-Infinity",
    ],
)
def test_invalid_prices_are_rejected(invalid_price):
    with pytest.raises(InvalidFruitPriceError):
        Apple(invalid_price)


@pytest.mark.parametrize(
    "invalid_price",
    [
        True,
        False,
        None,
        [],
        object(),
        "not-a-price",
    ],
)
def test_invalid_price_types_are_rejected(invalid_price):
    with pytest.raises(InvalidFruitPriceError):
        Apple(invalid_price)


def test_numeric_string_is_accepted():
    apple = Apple("180.50")

    assert apple.price_per_kg == Decimal("180.50")


def test_inventory_accepts_multiple_fruit_types():
    inventory = FruitInventory(
        [
            Apple(180),
            Banana(60),
            Orange(100),
        ]
    )

    assert len(inventory.fruits) == 3


def test_inventory_exposes_a_tuple():
    inventory = FruitInventory([Apple(180)])

    assert isinstance(inventory.fruits, tuple)


def test_inventory_rejects_non_fruit_objects():
    inventory = FruitInventory()

    with pytest.raises(TypeError):
        inventory.add_fruit("Apple")


def test_average_price():
    inventory = FruitInventory(
        [
            Apple(180),
            Banana(60),
            Orange(100),
        ]
    )

    assert inventory.average_price() == Decimal(340) / Decimal(3)


def test_empty_inventory_average_raises_exception():
    inventory = FruitInventory()

    with pytest.raises(EmptyInventoryError):
        inventory.average_price()


def test_find_by_name_is_case_insensitive():
    inventory = FruitInventory(
        [
            Apple(180),
            Banana(60),
            Apple(200),
        ]
    )

    matches = inventory.find_by_name("aPpLe")

    assert len(matches) == 2
    assert all(fruit.name == "Apple" for fruit in matches)


def test_find_by_name_returns_empty_list_when_missing():
    inventory = FruitInventory([Apple(180)])

    assert inventory.find_by_name("Mango") == []


def test_find_by_name_rejects_non_string():
    inventory = FruitInventory()

    with pytest.raises(TypeError):
        inventory.find_by_name(123)


def test_new_fruit_works_without_inventory_changes():
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

    inventory = FruitInventory([Mango(120)])

    assert inventory.fruits[0].name == "Mango"
    assert inventory.average_price() == Decimal("120")


def test_inventory_display(capsys):
    inventory = FruitInventory(
        [
            Apple(180),
            Banana(60),
        ]
    )

    inventory.display_inventory()
    output = capsys.readouterr().out

    assert "DHIDROID FRUIT INVENTORY" in output
    assert "Apple" in output
    assert "Banana" in output
    assert "Total entries" in output


def test_empty_inventory_display(capsys):
    inventory = FruitInventory()

    inventory.display_inventory()
    output = capsys.readouterr().out

    assert "inventory is empty" in output.lower()
