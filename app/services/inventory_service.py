from app.repositories.inventory_repo import InventoryRepository
from app.services.ml_service import ml_service
from app.schemas.schemas import ProductCreate, SalesCreate

class InventoryService:
    """Service layer for inventory management, coordinating between repositories and ML services."""
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    async def register_product(self, product_data: ProductCreate):
        """Register a new product in the system."""
        return await self.repo.create_product(product_data)

    async def record_sale(self, sales_data: SalesCreate):
        """Record a sales transaction and update stock."""
        return await self.repo.add_sales_record(sales_data)

    async def get_dashboard(self):
        """Retrieve a summary of system-wide inventory status."""
        return await self.repo.get_dashboard_summary()

    async def get_stockout_prediction(self, product_id: int):
        """
        Calculate the predicted days until a product runs out of stock.
        Uses historical sales data and current inventory levels.
        """
        product = await self.repo.db.get(Product, product_id)
        if not product or not product.inventory:
            return None
        
        avg_sales = await self.repo.get_average_daily_sales(product_id)
        # Standard lead time for prediction if not specified
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
