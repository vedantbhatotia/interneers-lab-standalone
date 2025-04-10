import pytest
from unittest.mock import MagicMock
from product.ProductCategoryService import ProductCategoryService
from product.Category_models import ProductCategory
from rest_framework.exceptions import ValidationError,NotFound


@pytest.fixture
def mock_repository():
    mock_repo = MagicMock()
    service = ProductCategoryService()
    service.repository = mock_repo
    return service, mock_repo


def test_create_category_success(mock_repository):
    service, repo = mock_repository
    repo.create_category.return_value = ProductCategory(title="Electronics", description="Gadgets and tech")
    
    result = service.create_category("Electronics", "Gadgets and tech")
    
    assert isinstance(result, ProductCategory)
    assert result.title == "Electronics"
    repo.create_category.assert_called_once()


def test_create_category_duplicate(mock_repository):
    service, repo = mock_repository
    from mongoengine.errors import NotUniqueError
    repo.create_category.side_effect = NotUniqueError()

    with pytest.raises(ValidationError) as exc:
        service.create_category("Electronics", "Duplicate")
    
    assert "already exists" in str(exc.value)


def test_get_category_by_id_success(mock_repository):
    service, repo = mock_repository
    repo.get_category_by_id.return_value = ProductCategory(id="123", title="Books", description="All kinds of books")

    result = service.get_category_by_id("123")
    assert result.title == "Books"
    repo.get_category_by_id.assert_called_once_with("123")


def test_get_category_by_id_not_found(mock_repository):
    service, repo = mock_repository
    repo.get_category_by_id.return_value = None

    with pytest.raises(NotFound) as exc:
        service.get_category_by_id("invalid-id")

    assert "not found" in str(exc.value)


def test_update_category_success(mock_repository):
    service, repo = mock_repository
    repo.update_category.return_value = ProductCategory(title="Updated", description="Updated description")

    result = service.update_category("123", title="Updated")
    assert result.title == "Updated"
    repo.update_category.assert_called_once()


def test_update_category_not_found(mock_repository):
    service, repo = mock_repository
    repo.update_category.return_value = None

    with pytest.raises(ValidationError) as exc:
        service.update_category("123", title="Non-existent")
    
    assert "not found" in str(exc.value)


def test_delete_category_success(mock_repository):
    service, repo = mock_repository
    repo.delete_category.return_value = True

    result = service.delete_category("123")
    assert result is True
    repo.delete_category.assert_called_once()


def test_delete_category_not_found(mock_repository):
    service, repo = mock_repository
    repo.delete_category.return_value = False

    with pytest.raises(ValidationError) as exc:
        service.delete_category("invalid-id")

    assert "not found" in str(exc.value)