from rest_framework.exceptions import ValidationError
from .ProductCategoryRepository import ProductCategoryRepository
from .Category_models import ProductCategory
from django.db.models.query import QuerySet
from mongoengine.errors import NotUniqueError
from django.db import transaction


class ProductCategoryService:
    def __init__(self):
        self.repository = ProductCategoryRepository()

    def create_category(self, title: str, description: str) -> ProductCategory:
       try:
            new_category = self.repository.create_category(title, description)
            return new_category
       except NotUniqueError:
            raise ValidationError({"title": "Category with this title already exists."})

    def list_categories(self) -> QuerySet:
        return self.repository.get_all_categories()

    def get_category_by_id(self, category_id: str) -> ProductCategory:
        category = self.repository.get_category_by_id(category_id)
        if not category:
            raise ValidationError({"category_id": f"Category with ID '{category_id}' not found."})
        return category

    def update_category(self, category_id: str, **kwargs) -> ProductCategory:
        # with transaction.atomic():

        category = self.repository.update_category(category_id, **kwargs)
        if not category:
            raise ValidationError({"category_id": f"Category with ID '{category_id}' not found."})
        return category

    def delete_category(self, category_id: str) -> bool:
        deleted = self.repository.delete_category(category_id)
        if not deleted:
            raise ValidationError({"id": f"Category with ID '{category_id}' not found."})
        return True