
import pytest
from delivery import calculate_delivery_cost


@pytest.mark.parametrize(
    "amount, distance, premium, expected",
    [
        # Бесплатная доставка при заказе от 5000
        (5000, 10, False, 0.0),
        (6000, 30, False, 0.0),

        # Проверка границ суммы заказа
        (4999.99, 10, False, 500.0),

        # Расстояние до 5 км включительно
        (1000, 0, False, 200.0),
        (1000, 5, False, 200.0),
        (1000, 5.01, False, 500.0),

        # Расстояние до 20 км включительно
        (1000, 20, False, 500.0),
        (1000, 20.01, False, 500.3),

        # Расстояние больше 20 км
        (1000, 30, False, 800.0),

        # Премиум-клиент получает скидку 50%
        (1000, 10, True, 250.0),
        (1000, 5, True, 100.0),
        (1000, 30, True, 400.0),

        # Бесплатная доставка и премиум
        (5000, 10, True, 0.0),

        # Нулевая сумма заказа
        (0, 10, False, 500.0),
    ],
)
def test_delivery_cost(amount, distance, premium, expected):
    result = calculate_delivery_cost(amount, distance, premium)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("amount", [-1, -0.01])
def test_negative_order_amount(amount):
    with pytest.raises(ValueError, match="order_amount"):
        calculate_delivery_cost(amount, 10, False)


@pytest.mark.parametrize("distance", [-1, -0.01])
def test_negative_distance(distance):
    with pytest.raises(ValueError, match="distance_km"):
        calculate_delivery_cost(1000, distance, False)
