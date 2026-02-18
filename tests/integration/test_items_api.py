from httpx import AsyncClient

BASE_URL = "/api/v1/items"


async def test_create_item(client: AsyncClient):
    response = await client.post(
        f"{BASE_URL}/",
        json={"name": "Test Item", "price": 19.99, "description": "A test item"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 19.99
    assert data["is_active"] is True
    assert "id" in data


async def test_create_item_invalid_price(client: AsyncClient):
    response = await client.post(f"{BASE_URL}/", json={"name": "Bad", "price": -5.0})
    assert response.status_code == 422


async def test_create_item_missing_name(client: AsyncClient):
    response = await client.post(f"{BASE_URL}/", json={"price": 10.0})
    assert response.status_code == 422


async def test_list_items_empty(client: AsyncClient):
    response = await client.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


async def test_list_items(client: AsyncClient):
    await client.post(f"{BASE_URL}/", json={"name": "A", "price": 1.0})
    await client.post(f"{BASE_URL}/", json={"name": "B", "price": 2.0})
    response = await client.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 2


async def test_list_items_pagination(client: AsyncClient):
    for i in range(5):
        await client.post(f"{BASE_URL}/", json={"name": f"Item {i}", "price": 1.0})
    response = await client.get(f"{BASE_URL}/", params={"skip": 2, "limit": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["skip"] == 2
    assert data["limit"] == 2


async def test_get_item(client: AsyncClient):
    create_resp = await client.post(
        f"{BASE_URL}/", json={"name": "Find Me", "price": 5.0}
    )
    item_id = create_resp.json()["id"]
    response = await client.get(f"{BASE_URL}/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Find Me"


async def test_get_item_not_found(client: AsyncClient):
    response = await client.get(f"{BASE_URL}/999")
    assert response.status_code == 404


async def test_update_item(client: AsyncClient):
    create_resp = await client.post(f"{BASE_URL}/", json={"name": "Old", "price": 1.0})
    item_id = create_resp.json()["id"]
    response = await client.put(
        f"{BASE_URL}/{item_id}", json={"name": "New", "price": 99.99}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New"
    assert data["price"] == 99.99


async def test_update_item_partial(client: AsyncClient):
    create_resp = await client.post(
        f"{BASE_URL}/", json={"name": "Partial", "price": 10.0}
    )
    item_id = create_resp.json()["id"]
    response = await client.put(f"{BASE_URL}/{item_id}", json={"name": "Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["price"] == 10.0


async def test_update_item_not_found(client: AsyncClient):
    response = await client.put(f"{BASE_URL}/999", json={"name": "Ghost"})
    assert response.status_code == 404


async def test_delete_item(client: AsyncClient):
    create_resp = await client.post(
        f"{BASE_URL}/", json={"name": "Delete Me", "price": 1.0}
    )
    item_id = create_resp.json()["id"]
    response = await client.delete(f"{BASE_URL}/{item_id}")
    assert response.status_code == 204
    # Verify it's gone
    get_resp = await client.get(f"{BASE_URL}/{item_id}")
    assert get_resp.status_code == 404


async def test_delete_item_not_found(client: AsyncClient):
    response = await client.delete(f"{BASE_URL}/999")
    assert response.status_code == 404
