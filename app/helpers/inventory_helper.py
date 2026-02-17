from datetime import datetime

def calculate_stockout_date(days_until_stockout: float) -> datetime:
    from datetime import timedelta
    return datetime.utcnow() + timedelta(days=days_until_stockout)

def format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_reorder_point(avg_daily_sales: float, lead_time: int, safety_stock: int = 10) -> float:
    return (avg_daily_sales * lead_time) + safety_stock

def calculate_safety_stock(max_daily_sales: float, max_lead_time: int, avg_daily_sales: float, avg_lead_time: int) -> float:
    """Standard safety stock formula: (Max Sales * Max Lead) - (Avg Sales * Avg Lead)"""
    return (max_daily_sales * max_lead_time) - (avg_daily_sales * avg_lead_time)

def calculate_economic_order_quantity(annual_demand: float, setup_cost: float, holding_cost: float) -> float:
    """EOQ formula: sqrt((2 * Demand * Setup Cost) / Holding Cost)"""
    import math
    if holding_cost <= 0:
        return 0.0
    return math.sqrt((2 * annual_demand * setup_cost) / holding_cost)

