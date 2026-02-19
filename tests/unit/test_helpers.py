from app.helpers.inventory_helper import (
    calculate_stockout_date,
    format_date,
    calculate_reorder_point,
    calculate_safety_stock,
    calculate_economic_order_quantity
)
from datetime import datetime, timedelta

def test_calculate_reorder_point():
    assert calculate_reorder_point(10.0, 5, 20) == 70.0

def test_calculate_safety_stock():
    # (Max Sales 20 * Max Lead 10) - (Avg Sales 10 * Avg Lead 5) = 200 - 50 = 150
    assert calculate_safety_stock(20, 10, 10, 5) == 150

def test_calculate_eoq():
    # sqrt((2 * 1000 * 50) / 2) = sqrt(50000) = 223.6...
    eoq = calculate_economic_order_quantity(1000, 50, 2)
    assert round(eoq, 1) == 223.6

def test_format_date():
    dt = datetime(2026, 1, 1, 12, 0, 0)
    assert format_date(dt) == "2026-01-01 12:00:00"
