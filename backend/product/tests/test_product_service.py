import pytest
from unittest.mock import MagicMock, patch
from product.ProductService import ProductService
from product.Product_models import Product
from product.Category_models import ProductCategory
from rest_framework.exceptions import ValidationError, NotFound

@pytest.fixture
def mock_repositories():
    mock_product_repo = MagicMock()
    mock_category_repo = MagicMock()

    service = ProductService()
    service.repository = mock_product_repo
    service.category_repository = mock_category_repo

    return service, mock_product_repo, mock_category_repo


@pytest.mark.parametrize(
    "name, desc, category_id, price, brand, stock, get_by_name_return, get_cat_return, create_return, should_raise, expected_error",
    [
        ("NewProduct", "desc", "1", 100, "Brand", 5,
         None,
         ProductCategory(id="1", title="Cat", description=""),
         Product(name="NewProduct"),
         False,
         None),
        ("Exists", "desc", "1", 100, "Brand", 5,
         Product(name="Exists"),
         ProductCategory(id="1", title="Cat", description=""),
         None,
         True,
         "Product already exists"),
        ("New", "desc", "invalid_id", 100, "Brand", 5,
         None,
         None,
         None,
         True,
         "Category with ID 'invalid_id' not found."),
    ]
)
def test_create_product_param(mock_repositories, name, desc, category_id, price, brand, stock,
                              get_by_name_return, get_cat_return, create_return,
                              should_raise, expected_error):
    service, product_repo, category_repo = mock_repositories
    product_repo.get_product_by_name.return_value = get_by_name_return
    category_repo.get_category_by_id.return_value = get_cat_return
    product_repo.create_product.return_value = create_return

    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            service.create_product(name, desc, category_id, price, brand, stock)
        assert expected_error in str(exc_info.value)
    else:
        result = service.create_product(name, desc, category_id, price, brand, stock)
        assert result.name == create_return.name
        product_repo.get_product_by_name.assert_called_once()
        category_repo.get_category_by_id.assert_called_once()
        product_repo.create_product.assert_called_once()


@pytest.mark.parametrize(
    "product_id, get_return, should_raise, expected_error",
    [
        ("123", Product(name="Test"), False, None),
        ("invalid-id", None, True, "Product with ID 'invalid-id' not found.")
    ]
)
def test_get_product_by_id_param(mock_repositories, product_id, get_return, should_raise, expected_error):
    service, product_repo, _ = mock_repositories
    product_repo.get_product_by_id.return_value = get_return

    if should_raise:
        with pytest.raises(NotFound) as exc_info:
            service.get_product_by_id(product_id)
        assert expected_error in str(exc_info.value)
    else:
        result = service.get_product_by_id(product_id)
        assert result.name == get_return.name
        product_repo.get_product_by_id.assert_called_once()


@pytest.mark.parametrize(
    "delete_return, product_id, should_raise, expected_error",
    [
        (True, "123", False, None),
        (False, "not-exist", True, "Product with ID 'not-exist' not found.")
    ]
)
def test_delete_product_param(mock_repositories, delete_return, product_id, should_raise, expected_error):
    service, product_repo, _ = mock_repositories
    product_repo.delete_product.return_value = delete_return

    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            service.delete_product(product_id)
        assert expected_error in str(exc_info.value)
    else:
        result = service.delete_product(product_id)
        assert result is True
        product_repo.delete_product.assert_called_once()




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
