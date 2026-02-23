from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.schemas import ProductCreate, SalesCreate
from app.repositories.inventory_repo import InventoryRepository
from app.services.inventory_service import InventoryService
from app.helpers.response_helper import standard_response
from app.models.models import User

router = APIRouter()

def get_inventory_service(db: AsyncSession = Depends(get_db)):
    repo = InventoryRepository(db)
    return InventoryService(repo)

@router.post("/products")
async def create_product(
    product_in: ProductCreate, 
    service: InventoryService = Depends(get_inventory_service),
    current_user: User = Depends(get_current_user)
):
    """
    Register a new product in the catalog.
    Initializes an inventory record with zero stock by default.
    """
    product = await service.register_product(product_in)
    return standard_response(data={"product_id": product.id, "sku": product.sku})

@router.post("/sales")
async def record_sale(
    sales_in: SalesCreate,
    service: InventoryService = Depends(get_inventory_service),
    current_user: User = Depends(get_current_user)
):
    """
    Log a new sales transaction.
    Automatically decrements the current stock level for the product.
    """
    sale = await service.record_sale(sales_in)
    return standard_response(data={"sale_id": sale.id})

@router.get("/prediction/{product_id}")
async def get_prediction(
    product_id: int,
    service: InventoryService = Depends(get_inventory_service),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve AI-driven stockout predictions for a specific product.
    Returns days until stockout and a status level (critical/stable).
    """
    prediction = await service.get_stockout_prediction(product_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Product not found")
    return standard_response(data=prediction)

@router.get("/dashboard")
async def get_dashboard(
    service: InventoryService = Depends(get_inventory_service),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch high-level inventory metrics for the manager dashboard.
    Includes total product counts and low-stock alert counts.
    """
    summary = await service.get_dashboard()
    return standard_response(data=summary)
