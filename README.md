# Лабораторна робота №3. Модульне тестування програмного коду (Unit Testing)

**Виконав:** Юдін Юрій, студент групи ПЗПІ-25  
**Дисципліна:** Основи програмної інженерії  
**Варіант виконання:** Індивідуальний за проєктом "PizzaFlow"

---

## 1. Тема та мета лабораторної роботи

### Тема
Модульне тестування програмного коду (Unit Testing).

### Мета
Набуття практичних навичок із написання модульних тестів із використанням промислових фреймворків тестування (pytest). Оволодіння формальними техніками проєктування тестів — еквівалентне розбиття (EP) та аналіз граничних значень (BVA). Досягнення покриття рядків коду (line coverage) не менше 80%.

---

## 2. Вихідний код реалізованого модуля (`discount.py`)

Цей модуль реалізує бізнес-логіку підрахунку знижок на замовлення піци в системі «PizzaFlow» та містить умовні розгалуження і механізми обробки винятків.

```python
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
```

---

## 3. Таблиця проєктування тестів (EP + BVA)

| Тест-кейс | Вхідні дані | Очікуваний результат | Техніка (EP/BVA) | Статус |
|------------|------------|---------------------|------------------|--------|
| TC-01 | customer_type="standard" | Об'єкт створено успішно | EP (Позитивний) | pass |
| TC-02 | customer_type="unknown" | ValueError (невідомий тип) | EP (Негативний) | pass |
| TC-03 | amount=-1 | ValueError (від'ємна сума) | BVA (Граничне значення -1) | pass |
| TC-04 | amount=0 | 0.0 (нульова сума) | BVA (Граничне значення 0) | pass |
| TC-05 | amount=0.01 | 0.0 (мінімальна сума) | BVA (Граничне значення 0.01) | pass |
| TC-06 | customer_type="standard", amount=1000 | 50.0 (знижка 5%) | EP (Позитивний) | pass |
| TC-07 | customer_type="premium", amount=1000 | 100.0 (знижка 10%) | EP (Позитивний) | pass |
| TC-08 | customer_type="vip", amount=1000 | 150.0 (знижка 15%) | EP (Позитивний) | pass |
| TC-09 | amount=200 (для standard) | 190.0 (фінальна вартість) | EP (Позитивний) | pass |
| TC-10 | amount=100, qty=10 | 95.0 (без додаткової знижки) | BVA (Гранична межа 10) | pass |
| TC-11 | amount=100, qty=11 | 92.15 (додаткова знижка 3%) | BVA (Межа 11, qty > 10) | pass |
| TC-12 | amount=100, qty=-1 | ValueError (від'ємна кількість) | EP (Негативний) | pass |

---

## 4. Вихідний код тестового набору (`test_discount.py`)

Тести розроблені за патерном AAA (Arrange, Act, Assert) та покривають усі визначені класи еквівалентності й граничні значення.

```python
import pytest
from discount import DiscountCalculator

# --- Тести конструктора ---

def test_valid_customer_types():
    # Arrange & Act & Assert (EP: Допустимі класи)
    for ct in ("standard", "premium", "vip"):
        calc = DiscountCalculator(ct)
        assert calc.customer_type == ct

def test_invalid_customer_type():
    # Arrange & Act & Assert (EP: Недопустимий клас)
    with pytest.raises(ValueError):
        DiscountCalculator("unknown")

# --- Тести calculate ---

def test_calculate_negative_amount():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act & Assert (BVA: Від'ємна межа -1)
    with pytest.raises(ValueError):
        calc.calculate(-1)

def test_calculate_zero_amount():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act
    result = calc.calculate(0)

    # Assert
    assert result == 0.0

def test_calculate_minimal_positive():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act
    result = calc.calculate(0.01)

    # Assert
    assert result == 0.0

def test_calculate_standard_1000():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act
    result = calc.calculate(1000)

    # Assert
    assert result == 50.0

def test_calculate_premium_1000():
    # Arrange
    calc = DiscountCalculator("premium")

    # Act
    result = calc.calculate(1000)

    # Assert
    assert result == 100.0

def test_calculate_vip_1000():
    # Arrange
    calc = DiscountCalculator("vip")

    # Act
    result = calc.calculate(1000)

    # Assert
    assert result == 150.0

# --- Тести apply_discount ---

def test_apply_discount_standard():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act
    result = calc.apply_discount(200)

    # Assert
    assert result == 190.0

# --- Тести bulk_discount ---

def test_bulk_no_extra_discount():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act
    result = calc.bulk_discount(100, 10)

    # Assert
    assert result == 95.0

def test_bulk_with_extra_discount():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act
    result = calc.bulk_discount(100, 11)

    # Assert
    assert result == 92.15

def test_bulk_negative_qty():
    # Arrange
    calc = DiscountCalculator("standard")

    # Act & Assert
    with pytest.raises(ValueError):
        calc.bulk_discount(100, -1)
```

---

## 5. Звіт покриття коду (Code Coverage)

Для оцінки покриття коду було використано інструмент `coverage.py` разом із фреймворком `pytest`.

Команда запуску:

```bash
python -m pytest --cov=discount --cov-report=term
```

Результат виконання:

```text
Name              Stmts   Miss  Cover
-------------------------------------
discount.py          22      0   100%
-------------------------------------
TOTAL                22      0   100%

==================== 12 passed in 0.50s ====================
```

### Скриншот виконаних тестів та покриття

*Нижче у звіті необхідно вставити скриншот консолі з результатами запуску тестів та показником покриття 100%.*

### Аналіз покриття

Завдяки системному застосуванню технік еквівалентного розбиття (EP) та аналізу граничних значень (BVA) було перевірено всі гілки виконання програмного коду. Тестовий набір забезпечив 100% line coverage, що значно перевищує мінімальну вимогу методичних вказівок (80%).

---

## 6. Посилання на Git-репозиторій

Код реалізованого модуля, тестовий набір та HTML-звіт про покриття розміщені у публічному репозиторії GitHub.

**Посилання на репозиторій:**

```
(https://github.com/yuriiiudin-ui/LR03_OPI)
```

---

## 7. Висновки

Під час виконання лабораторної роботи №3 було успішно засвоєно та застосовано на практиці методологію модульного тестування (Unit Testing) за допомогою фреймворку `pytest` та інструменту `coverage.py`.

На основі розробленої раніше архітектури проєкту «PizzaFlow» було реалізовано програмний модуль калькулятора знижок. За допомогою формальних інженерних технік — еквівалентного розбиття (EP) та аналізу граничних значень (BVA) — спроєктовано й реалізовано 12 автоматизованих тест-кейсів, структурованих відповідно до патерна AAA (Arrange, Act, Assert).

Результати тестування підтвердили коректність роботи всіх функцій модуля, а звіт про покриття коду засвідчив досягнення 100% line coverage. Це гарантує високу надійність реалізованої бізнес-логіки, мінімізує ризик виникнення регресійних помилок та створює надійну основу для подальшого розвитку й рефакторингу системи.
