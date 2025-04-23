import pytest
from rest_framework.test import APIClient
from rest_framework import status

# enable access to the test DB
pytestmark = pytest.mark.django_db
client = APIClient()

def test_create_category():
    data = {
        "title": "Integration Test Category",
        "description": "Created via Integration test"
    }
    response = client.post("/api/categories/", data, format="json")
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "Integration Test Category"


def test_list_categories():
    response = client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("Test" in cat.get("title", "") for cat in data)


def test_get_category_detail():
    response = client.get("/api/categories/")
    categories = response.json()
    assert categories, "No categories found."
    category_id = categories[0]["id"]
    category_detail = client.get(f"/api/categories/{category_id}/")
    assert category_detail.status_code == 200


def test_update_category():
    categories = client.get("/api/categories/").json()
    if not categories:
        pytest.skip("No categories available to update.")
    category_id = categories[0]["id"]

    updated_data = {
        "title": "Updated Test Category",
        "description": "Updated via API"
    }

    response = client.put(f"/api/categories/{category_id}/", updated_data, format="json")
    assert response.status_code in (200, 201)
    assert response.json()["title"] == "Updated Test Category"


def test_delete_category():
    response = client.post("/api/categories/", {
        "title": "To Be Deleted",
        "description": "Temp"
    }, format="json")
    assert response.status_code in (200, 201)
    category_id = response.json()["id"]

    delete_response = client.delete(f"/api/categories/{category_id}/")
    assert delete_response.status_code in (200, 204)

    get_response = client.get(f"/api/categories/{category_id}/")
    assert get_response.status_code == 404



def test_create_product():
    cat_list = client.get("/api/categories/")
    categories = cat_list.json()
    assert categories, "No categories available to assign product to."
    category_id = categories[0]["id"]

    payload_product = {
        "name": "Integration Test Product",
        "description": "Product created via API test",
        "price": 49.99,
        "brand": "TestBrand",
        "stock": 25,
        "category": category_id
    }
    response = client.post("/api/products/", payload_product, format="json")
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["name"] == "Integration Test Product"


def test_list_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_product_detail():
    products = client.get("/api/products/").json()
    if not products:
        pytest.skip("No products available to get detail.")
    product_id = products[0]["id"]
    response = client.get(f"/api/products/{product_id}/")
    assert response.status_code == 200
    assert "name" in response.json()

def test_update_product():
    products = client.get("/api/products/").json()
    if not products:
        pytest.skip("No products available to update.")
    
    product = products[0]
    category_id = product["category_object"]["id"]
    # print(category_id)
    updated_data = {
        "name": "Updated Product Name",
        "description": "Updated Description",
        "price": 99.99,
        "brand": "UpdatedBrand",
        "stock": 50,
        "category": category_id,
    }
    response = client.put(f"/api/products/{product['id']}/", updated_data, format="json")
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == "Updated Product Name"



def test_delete_product():
    products = client.get("/api/products/").json()
    if not products:
        pytest.skip("No products available to delete.")
    product_id = products[0]["id"]

    response = client.delete(f"/api/products/{product_id}/")
    assert response.status_code in (200, 204)

    get_response = client.get(f"/api/products/{product_id}/")
    assert get_response.status_code == 404


