import uuid


def create_sample_category(client):

    res = client.post(
        "/categories",
        json={
            "name": "Electronics",
            "description": "Electronic items"
        }
    )

    assert res.status_code == 201
    return res.json()["id"]


def test_create_product(client):

    category_id = create_sample_category(client)

    response = client.post(
        "/products",
        json={
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": "1200.00",
            "sku": "LAP-001",
            "category_ids": [category_id]
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Laptop"
    assert data["sku"] == "LAP-001"


def test_get_product(client):

    res = client.post(
        "/products",
        json={
            "name": "Phone",
            "description": "Smartphone",
            "price": "800.00",
            "sku": "PHN-001"
        }
    )

    product_id = res.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Phone"


def test_search_products(client):

    client.post(
        "/products",
        json={
            "name": "Tablet",
            "description": "Android tablet",
            "price": "400.00",
            "sku": "TAB-001"
        }
    )

    response = client.get("/products/search?q=tablet")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_delete_product(client):

    res = client.post(
        "/products",
        json={
            "name": "Mouse",
            "description": "Wireless mouse",
            "price": "50.00",
            "sku": "MOU-001"
        }
    )

    product_id = res.json()["id"]

    delete_res = client.delete(f"/products/{product_id}")

    assert delete_res.status_code == 204

    get_res = client.get(f"/products/{product_id}")

    assert get_res.status_code == 404
