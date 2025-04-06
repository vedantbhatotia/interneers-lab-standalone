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


# AAA Pattern for writing unit test
# Arrange=>Sets up mocks and dependencies
# Act=>Calls the actual method to be tested
# Assert=>Verifies the expected behavior



#CREATE PRODUCT 
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



#GET PRODUCTS
def test_get_product_by_id_success(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_id.return_value = Product(name="Test")

    result = service.get_product_by_id("123")
    assert result.name == "Test"
    product_repo.get_product_by_id.assert_called_once_with("123")

def test_get_product_by_id_not_found(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_id.return_value = None

    with pytest.raises(ValidationError):
        service.get_product_by_id("invalid-id")








# # def test_update_product_success(mock_repositories):
# #     service, product_repo, category_repo = mock_repositories
# #     category_repo.get_category_by_id.return_value = ProductCategory(id="1", title="Cat", description="")
# #     product_repo.update_product.return_value = Product(name="Updated")

# #     result = service.update_product("123", category="1", name="Updated")
# #     assert result.name == "Updated"
# #     product_repo.update_product.assert_called_once()

# def test_update_product_no_fields(mock_repositories):
#     service, _, _ = mock_repositories

#     with pytest.raises(ValidationError):
#         service.update_product("123")

# def test_update_product_invalid_category(mock_repositories):
#     service, _, category_repo = mock_repositories
#     category_repo.get_category_by_id.return_value = None

#     with pytest.raises(ValidationError):
#         service.update_product("123", category="invalid")

# def test_update_product_not_found(mock_repositories):
#     service, product_repo, category_repo = mock_repositories
#     category_repo.get_category_by_id.return_value = ProductCategory(id="1", title="Cat", description="")
#     product_repo.update_product.return_value = None

#     with pytest.raises(ValidationError):
#         service.update_product("123", category="1", name="New")






#DELETE PRODUCT
def test_delete_product_success(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.delete_product.return_value = True

    result = service.delete_product("123")
    assert result == True
    product_repo.delete_product.assert_called_once_with("123")

def test_delete_product_not_found(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.delete_product.return_value = False

    with pytest.raises(ValidationError):
        service.delete_product("not-exist")
