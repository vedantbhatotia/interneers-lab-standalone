import pytest
from unittest.mock import MagicMock
from product.ProductCategoryService import ProductCategoryService
from product.Category_models import ProductCategory
from rest_framework.exceptions import ValidationError, NotFound
from mongoengine.errors import NotUniqueError

@pytest.fixture
def mock_repository():
    mock_repo = MagicMock()
    service = ProductCategoryService()
    service.repository = mock_repo
    return service, mock_repo


#parameterisation enables to run the same test logic but with different inputs and expected outputs avoiding code duplication and redundancy

# Create Category
@pytest.mark.parametrize(
    "title, description, mock_return, side_effect, should_raise, expected_exception_text",
    [
        ("Electronics", "Gadgets and tech", ProductCategory(title="Electronics", description="Gadgets and Tech"), None, False, None),
        ("Electronics", "Duplicate", None, NotUniqueError(), True, "already exists")
    ]
)
def test_create_category_cases(mock_repository, title, description, mock_return, side_effect, should_raise, expected_exception_text):
    service, repo = mock_repository
    repo.create_category.return_value = mock_return
    repo.create_category.side_effect = side_effect

    if should_raise:
        with pytest.raises(ValidationError) as exc:
            service.create_category(title, description)
        assert expected_exception_text in str(exc.value)
    else:
        result = service.create_category(title, description)
        assert isinstance(result, ProductCategory)
        assert result.title == title
        repo.create_category.assert_called_once()


# Get Category by ID
@pytest.mark.parametrize(
    "category_id, mock_return, should_raise, expected_exception_text",
    [
        ("123", ProductCategory(id="123", title="Books", description="All kinds of books"), False, None),
        ("invalid-id", None, True, "not found")
    ]
)
def test_get_category_by_id_cases(mock_repository, category_id, mock_return, should_raise, expected_exception_text):
    service, repo = mock_repository
    repo.get_category_by_id.return_value = mock_return

    if should_raise:
        with pytest.raises(NotFound) as exc:
            service.get_category_by_id(category_id)
        assert expected_exception_text in str(exc.value)
    else:
        result = service.get_category_by_id(category_id)
        assert result.title == mock_return.title
        repo.get_category_by_id.assert_called_once_with(category_id)


# Update Category
@pytest.mark.parametrize(
    "category_id, update_data, mock_return, should_raise, expected_exception_text",
    [
        ("123", {"title": "Updated"}, ProductCategory(title="Updated", description="Updated description"), False, None),
        ("123", {"title": "Non-existent"}, None, True, "not found")
    ]
)
def test_update_category_cases(mock_repository, category_id, update_data, mock_return, should_raise, expected_exception_text):
    service, repo = mock_repository
    repo.update_category.return_value = mock_return

    if should_raise:
        with pytest.raises(ValidationError) as exc:
            service.update_category(category_id, **update_data)
        assert expected_exception_text in str(exc.value)
    else:
        result = service.update_category(category_id, **update_data)
        assert result.title == update_data["title"]
        repo.update_category.assert_called_once()


# Delete Category
@pytest.mark.parametrize(
    "category_id, mock_return, should_raise, expected_exception_text",
    [
        ("123", True, False, None),
        ("invalid-id", False, True, "not found")
    ]
)
def test_delete_category_cases(mock_repository, category_id, mock_return, should_raise, expected_exception_text):
    service, repo = mock_repository
    repo.delete_category.return_value = mock_return

    if should_raise:
        with pytest.raises(ValidationError) as exc:
            service.delete_category(category_id)
        assert expected_exception_text in str(exc.value)
    else:
        result = service.delete_category(category_id)
        assert result is True
        repo.delete_category.assert_called_once()
