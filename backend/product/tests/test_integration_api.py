import pytest
from rest_framework.test import APIClient
from product.Product_models import Product
from product.Category_models import ProductCategory

#enable the test db access
pytestmark = pytest.mark.django_db

client = APIClient()

def test_list_categories():
    response = client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)
    # assert any("TestCat" for cat.get("title","") 
    assert any("TestCat" in cat.get("title","") for cat in data)


def test_create_category():
    data = {
        "title":"Integration Test Category",
        "description":"Created via Integration test"
    }
    response = client.post("/api/categories/",data,format="json")
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["title"] == "Integration Test Category"


def test_get_category_detail():
    response = client.get("/api/categories/")
    category_id = response.json()[0]["id"]
    category_detail = client.get(f"/api/categories/{category_id}/")
    assert category_detail.status_code == 200

