import pytest
from discount import DiscountCalculator

# --- Тести конструктора ---

def test_valid_customer_types():
    for ct in ("standard", "premium", "vip"):
        calc = DiscountCalculator(ct)
        assert calc.customer_type == ct

def test_invalid_customer_type():
    with pytest.raises(ValueError):
        DiscountCalculator("unknown")

# --- Тести calculate ---

def test_calculate_negative_amount():
    calc = DiscountCalculator("standard")
    with pytest.raises(ValueError):
        calc.calculate(-1)

def test_calculate_zero_amount():
    calc = DiscountCalculator("standard")
    result = calc.calculate(0)
    assert result == 0.0

def test_calculate_minimal_positive():
    calc = DiscountCalculator("standard")
    result = calc.calculate(0.01)
    assert result == 0.0

def test_calculate_standard_1000():
    calc = DiscountCalculator("standard")
    result = calc.calculate(1000)
    assert result == 50.0

def test_calculate_premium_1000():
    calc = DiscountCalculator("premium")
    result = calc.calculate(1000)
    assert result == 100.0

def test_calculate_vip_1000():
    calc = DiscountCalculator("vip")
    result = calc.calculate(1000)
    assert result == 150.0

# --- Тести apply_discount ---

def test_apply_discount_standard():
    calc = DiscountCalculator("standard")
    result = calc.apply_discount(200)
    assert result == 190.0

# --- Тести bulk_discount ---

def test_bulk_no_extra_discount():
    calc = DiscountCalculator("standard")
    result = calc.bulk_discount(100, 10)
    assert result == 95.0

def test_bulk_with_extra_discount():
    calc = DiscountCalculator("standard")
    result = calc.bulk_discount(100, 11)
    assert result == 92.15

def test_bulk_negative_qty():
    calc = DiscountCalculator("standard")
    with pytest.raises(ValueError):
        calc.bulk_discount(100, -1)