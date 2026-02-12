from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Product, InventoryLevel, SalesHistory
from app.schemas.schemas import ProductCreate, SalesCreate
from datetime import datetime

class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_products(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_product_by_sku(self, sku: str):
        result = await self.db.execute(select(Product).filter(Product.sku == sku))
        return result.scalars().first()

    async def create_product(self, product_data: ProductCreate):
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        await self.db.flush()
        # Initialize inventory level
        db_inventory = InventoryLevel(product_id=db_product.id, current_stock=0)
        self.db.add(db_inventory)
        return db_product

    async def update_inventory(self, product_id: int, quantity_change: int):
        result = await self.db.execute(select(InventoryLevel).filter(InventoryLevel.product_id == product_id))
        inventory = result.scalars().first()
        if inventory:
            inventory.current_stock += quantity_change
            return inventory
        return None

    async def add_sales_record(self, sales_data: SalesCreate):
        db_sales = SalesHistory(**sales_data.model_dump())
        self.db.add(db_sales)
        # Update stock
        await self.update_inventory(sales_data.product_id, -sales_data.quantity)
        return db_sales

    async def get_dashboard_summary(self):
        # Total products
        total_products_res = await self.db.execute(select(Product))
        total_products = len(total_products_res.scalars().all())
        
        # Low stock items
        low_stock_res = await self.db.execute(
            select(InventoryLevel).filter(InventoryLevel.current_stock <= InventoryLevel.min_stock)
        )
        low_stock_items = len(low_stock_res.scalars().all())
        
        return {
            "total_products": total_products,
            "low_stock_alerts": low_stock_items
        }

    async def get_average_daily_sales(self, product_id: int, days: int = 30):
        # Dummy calculation for now, in real app would use group by date
        result = await self.db.execute(
            select(SalesHistory).filter(SalesHistory.product_id == product_id)
        )
        sales = result.scalars().all()
        total_qty = sum(s.quantity for s in sales)
        return total_qty / days if days > 0 else 0
