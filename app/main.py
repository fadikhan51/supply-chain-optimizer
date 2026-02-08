from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.inventory import router as inventory_router
from app.db.session import engine, Base

app = FastAPI(
    title="Predictive Supply Chain Optimizer",
    description="AI-powered supply chain management API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # For production, use Alembic migrations. For this MVP, we create all.
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["inventory"])

@app.get("/")
async def root():
    return {"message": "Welcome to Predictive Supply Chain Optimizer API"}
