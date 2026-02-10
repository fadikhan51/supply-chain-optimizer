from datetime import datetime

def calculate_stockout_date(days_until_stockout: float) -> datetime:
    from datetime import timedelta
    return datetime.utcnow() + timedelta(days=days_until_stockout)

def format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_reorder_point(avg_daily_sales: float, lead_time: int, safety_stock: int = 10) -> float:
    return (avg_daily_sales * lead_time) + safety_stock
