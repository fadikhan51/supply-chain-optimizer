from app.repositories.inventory_repo import InventoryRepository
from app.services.ml_service import ml_service
from app.schemas.schemas import ProductCreate, SalesCreate

class InventoryService:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def register_product(self, product_data: ProductCreate):
        return await self.repo.create_product(product_data)

    async def record_sale(self, sales_data: SalesCreate):
        return await self.repo.add_sales_record(sales_data)

    async def get_dashboard(self):
        return await self.repo.get_dashboard_summary()

    async def get_stockout_prediction(self, product_id: int):
        product = await self.repo.db.get(Product, product_id)
        if not product or not product.inventory:
            return None
        
        avg_sales = await self.repo.get_average_daily_sales(product_id)
        # Mock lead time or get from product if defined
        lead_time = 5 
        
        prediction = ml_service.predict_stockout(
            product.inventory.current_stock,
            avg_sales,
            lead_time
        )
        
        return {
            "product_id": product.id,
            "sku": product.sku,
            "days_until_stockout": prediction,
            "status": "critical" if prediction < 3 else "stable"
        }
from app.models.models import Product
