import pytest
from unittest.mock import MagicMock
from rest_framework.exceptions import ValidationError


from product.ProductService import ProductService
from product.Product_models import Product
from product.Category_models import ProductCategory


@pytest.fixture
def mock_repositories():
    """ set up the mocked repositories """
    mock_product_repo = MagicMock()
    mock_category_repo = MagicMock()
    
    service = ProductService()
    service.repository = mock_product_repo
    service.category_repository = mock_category_repo

    return service,mock_category_repo,mock_product_repo



#AAA Pattern for writing unit test
#Arrange=>Sets up mocks and dependencies
#Act=>Calls the actual method to be tested
#Assert=>Verifies the expected behavior

def test_create_product_success(mock_repositories):
    service,mock_category_repo,mock_product_repo = mock_repositories

    mock_product_repo.get_product_by_name.return_value = None
    mock_category_repo.get_category_by_id.return_value = ProductCategory(id = "123",title = "testCategory",description= "")

    mock_product_repo.create_product.return_value = Product(name="TestProduct")


    result = service.create_product(
        name = "TestProduct",
        description="Test description",
        category="123",
        price=100,
        brand="TestBrand",
        stock=50
    )

    assert result.name == "TestProduct"
    mock_product_repo.get_product_by_name.assert_called_once_with("TestProduct")
    mock_category_repo.get_category_by_id.assert_called_once_with("123")
    mock_product_repo.create_product.assert_called_once()