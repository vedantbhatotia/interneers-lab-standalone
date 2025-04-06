import pytest
from unittest.mock import MagicMock
from product.ProductService import ProductService
from product.Product_models import Product
from product.Category_models import ProductCategory
from rest_framework.exceptions import ValidationError

@pytest.fixture
def mock_repositories():
    mock_product_repo = MagicMock()
    mock_category_repo = MagicMock()

    service = ProductService()
    service.repository = mock_product_repo
    service.category_repository = mock_category_repo

    return service, mock_product_repo, mock_category_repo


# #AAA Pattern for writing unit test
# #Arrange=>Sets up mocks and dependencies
# #Act=>Calls the actual method to be tested
# #Assert=>Verifies the expected behavior

def test_create_product_success(mock_repositories):
    service, product_repo, category_repo = mock_repositories

    product_repo.get_product_by_name.return_value = None
    category_repo.get_category_by_id.return_value = ProductCategory(id="1", title="Cat", description="")
    product_repo.create_product.return_value = Product(name="NewProduct")

    result = service.create_product("NewProduct", "desc", "1", 100, "Brand", 5)

    assert result.name == "NewProduct"
    product_repo.get_product_by_name.assert_called_once_with("NewProduct")
    category_repo.get_category_by_id.assert_called_once_with("1")
    product_repo.create_product.assert_called_once()

def test_create_product_duplicate_name(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_name.return_value = Product(name="Exists")

    with pytest.raises(ValidationError):
        service.create_product("Exists", "desc", "1", 100, "Brand", 5)

def test_create_product_invalid_category(mock_repositories):
    service, product_repo, category_repo = mock_repositories
    product_repo.get_product_by_name.return_value = None
    category_repo.get_category_by_id.return_value = None

    with pytest.raises(ValidationError):
        service.create_product("New", "desc", "invalid_id", 100, "Brand", 5)

