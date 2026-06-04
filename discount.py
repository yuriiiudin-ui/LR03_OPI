class DiscountCalculator:
    """Калькулятор знижок за типом клієнта та сумою замовлення піци."""

    RATES = {
        "standard": 0.05,
        "premium": 0.10,
        "vip": 0.15,
    }

    def __init__(self, customer_type: str):
        if customer_type not in self.RATES:
            raise ValueError(f"Unknown type: {customer_type}")
        self.customer_type = customer_type

    def calculate(self, amount: float) -> float:
        """Обчислює суму знижки."""
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if amount == 0:
            return 0.0
        return round(amount * self.RATES[self.customer_type], 2)

    def apply_discount(self, amount: float) -> float:
        """Повертає суму після застосування знижки."""
        discount = self.calculate(amount)
        return round(amount - discount, 2)

    def bulk_discount(self, amount: float, qty: int) -> float:
        """Додаткова знижка 3% при кількості піц > 10 одиниць."""
        base = self.apply_discount(amount)
        if qty < 0:
            raise ValueError("Quantity cannot be negative")
        if qty > 10:
            return round(base * 0.97, 2)
        return base