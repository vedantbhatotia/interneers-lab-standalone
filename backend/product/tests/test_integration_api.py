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