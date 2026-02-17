from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.inventory import router as inventory_router
from app.db.session import engine, Base
from app.core.logging_config import setup_logging

setup_logging()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Predictive Supply Chain Optimizer",
    description="AI-powered supply chain management API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["inventory"])

@app.get("/")
async def root():
    return {"message": "Welcome to Predictive Supply Chain Optimizer API"}
