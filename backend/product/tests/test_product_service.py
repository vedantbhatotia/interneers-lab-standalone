import pytest
from unittest.mock import MagicMock, patch
from product.ProductService import ProductService
from product.Product_models import Product
from product.Category_models import ProductCategory
from rest_framework.exceptions import ValidationError,NotFound


@pytest.fixture
def mock_repositories():
    mock_product_repo = MagicMock()
    mock_category_repo = MagicMock()

    service = ProductService()
    service.repository = mock_product_repo
    service.category_repository = mock_category_repo

    return service, mock_product_repo, mock_category_repo


def test_create_product_success(mock_repositories):
    service, product_repo, category_repo = mock_repositories
    product_repo.get_product_by_name.return_value = None
    category_repo.get_category_by_id.return_value = ProductCategory(id="1", title="Cat", description="")
    product_repo.create_product.return_value = Product(name="NewProduct")

    result = service.create_product("NewProduct", "desc", "1", 100, "Brand", 5)

    assert result.name == "NewProduct"
    product_repo.get_product_by_name.assert_called_once()
    category_repo.get_category_by_id.assert_called_once()
    product_repo.create_product.assert_called_once()


def test_create_product_duplicate_name(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_name.return_value = Product(name="Exists")

    with pytest.raises(ValidationError) as exc_info:
        service.create_product("Exists", "desc", "1", 100, "Brand", 5)

    assert "Product already exists" in str(exc_info.value)


def test_create_product_invalid_category(mock_repositories):
    service, product_repo, category_repo = mock_repositories
    product_repo.get_product_by_name.return_value = None
    category_repo.get_category_by_id.return_value = None

    with pytest.raises(ValidationError) as exc_info:
        service.create_product("New", "desc", "invalid_id", 100, "Brand", 5)

    assert "Category with ID 'invalid_id' not found." in str(exc_info.value)


def test_get_product_by_id_success(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_id.return_value = Product(name="Test")

    result = service.get_product_by_id("123")

    assert result.name == "Test"
    product_repo.get_product_by_id.assert_called_once()


def test_get_product_by_id_not_found(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_id.return_value = None

    with pytest.raises(NotFound) as exc_info:
        service.get_product_by_id("invalid-id")

    assert "Product with ID 'invalid-id' not found." in str(exc_info.value)


@patch("product.ProductService.Product")
def test_update_product_success(mock_product_model, mock_repositories):
    service, product_repo, category_repo = mock_repositories
    mock_session = MagicMock()
    mock_client = MagicMock()
    mock_database = MagicMock()
    mock_collection = MagicMock()

    mock_product_model._get_collection.return_value = mock_collection
    mock_collection.database = mock_database
    mock_database.client = mock_client
    mock_client.start_session.return_value.__enter__.return_value = mock_session
    mock_session.start_transaction.return_value.__enter__.return_value = MagicMock()

    category_repo.get_category_by_id.return_value = ProductCategory(id="1", title="Cat", description="")
    product_repo.update_product.return_value = Product(name="UpdatedProduct")

    result = service.update_product("123", category="1", name="UpdatedProduct")

    assert result.name == "UpdatedProduct"
    category_repo.get_category_by_id.assert_called_once()
    product_repo.update_product.assert_called_once()


def test_update_product_no_fields(mock_repositories):
    service, _, _ = mock_repositories

    with pytest.raises(ValidationError) as exc_info:
        service.update_product("123")

    assert "No update fields provided." in str(exc_info.value)


def test_update_product_invalid_category(mock_repositories):
    service, _, category_repo = mock_repositories
    category_repo.get_category_by_id.return_value = None

    with pytest.raises(ValidationError) as exc_info:
        service.update_product("123", category="invalid")

    assert "Category with ID 'invalid' not found." in str(exc_info.value)


@patch("product.ProductService.Product")
def test_update_product_not_found(mock_product_model, mock_repositories):
    service, product_repo, category_repo = mock_repositories
    mock_session = MagicMock()
    mock_client = MagicMock()
    mock_database = MagicMock()
    mock_collection = MagicMock()

    mock_product_model._get_collection.return_value = mock_collection
    mock_collection.database = mock_database
    mock_database.client = mock_client
    mock_client.start_session.return_value.__enter__.return_value = mock_session
    mock_session.start_transaction.return_value.__enter__.return_value = MagicMock()

    category_repo.get_category_by_id.return_value = ProductCategory(id="1", title="Cat", description="")
    product_repo.update_product.return_value = None

    with pytest.raises(ValidationError) as exc_info:
        service.update_product("123", category="1", name="New")

    assert "Product with ID '123' not found." in str(exc_info.value)


def test_delete_product_success(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.delete_product.return_value = True

    result = service.delete_product("123")

    assert result is True
    product_repo.delete_product.assert_called_once()


def test_delete_product_not_found(mock_repositories):
    service, product_repo, _ = mock_repositories
    product_repo.delete_product.return_value = False

    with pytest.raises(ValidationError) as exc_info:
        service.delete_product("not-exist")

    assert "Product with ID 'not-exist' not found." in str(exc_info.value)


