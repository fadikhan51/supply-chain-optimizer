import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_product_and_record_sale(client: AsyncClient):
    # 1. Register user
    reg_resp = await client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "role": "admin"
    })
    assert reg_resp.status_code == 200
    
    # 2. Login
    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "password123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Product
    prod_resp = await client.post("/api/v1/inventory/products", json={
        "sku": "ITEM001",
        "name": "Widget A",
        "category": "Electronics"
    }, headers=headers)
    assert prod_resp.status_code == 200
    product_id = prod_resp.json()["data"]["product_id"]
    
    # 4. Record Sale
    sale_resp = await client.post("/api/v1/inventory/sales", json={
        "product_id": product_id,
        "quantity": 5
    }, headers=headers)
    assert sale_resp.status_code == 200
    
    # 5. Get Prediction
    pred_resp = await client.get(f"/api/v1/inventory/prediction/{product_id}", headers=headers)
    assert pred_resp.status_code == 200
    assert "days_until_stockout" in pred_resp.json()["data"]
