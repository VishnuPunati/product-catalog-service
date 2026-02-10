def test_create_category(client):

    response = client.post(
        "/categories",
        json={
            "name": "Books",
            "description": "Book category"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Books"


def test_get_category(client):

    res = client.post(
        "/categories",
        json={
            "name": "Movies",
            "description": "Movie category"
        }
    )

    category_id = res.json()["id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Movies"


def test_delete_category(client):

    res = client.post(
        "/categories",
        json={
            "name": "Music",
            "description": "Music category"
        }
    )

    category_id = res.json()["id"]

    delete_res = client.delete(f"/categories/{category_id}")

    assert delete_res.status_code == 204
