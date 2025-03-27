from rest_framework.exceptions import ValidationError
from .repositories import ProductRepository, ProductCategoryRepository
from .models import Product, ProductCategory
from django.db.models.query import QuerySet
from mongoengine.errors import NotUniqueError
from rest_framework.response import Response
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
        category = self.repository.update_category(category_id, **kwargs)
        if not category:
            raise ValidationError({"category_id": f"Category with ID '{category_id}' not found."})
        return category

    def delete_category(self, category_id: str) -> bool:
        deleted = self.repository.delete_category(category_id)
        if not deleted:
            raise ValidationError({"id": f"Category with ID '{category_id}' not found."})
        return True



class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.category_repository = ProductCategoryRepository()

    def create_product(self, name: str, description: str, category, price: float, brand: str, stock: int) -> Product:
        if self.repository.get_product_by_name(name):
            raise ValidationError({"name": "Product already exists"})

        # Ensure the category is a ProductCategory instance.
        if not isinstance(category, ProductCategory):
            # Lookup by id using the repository.
            category_obj = self.category_repository.get_category_by_id(category)
            if not category_obj:
                raise ValidationError({"category": f"Category with id '{category}' not found."})
        else:
            category_obj = category

        return self.repository.create_product(name, description, category_obj, price, brand, stock)

    
    def get_product_by_id(self, product_id: str) -> Product:
        product = self.repository.get_product_by_id(product_id)
        if not product:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return product

    def list_products(self) ->QuerySet:
        return self.repository.get_all_products()

    def update_product(self, product_id: str, **kwargs) -> Product:
        if not kwargs:
            raise ValidationError({"error": "No update fields provided."})
        
        if "category" in kwargs:
            category = self.category_repository.get_category_by_id(kwargs["category"])
            if not category:
                raise ValidationError({"category": f"Category with ID '{kwargs['category']}' not found."})
            kwargs["category"] = category

        updated = self.repository.update_product(product_id, **kwargs)
        if not updated:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return updated

    def delete_product(self, product_id: str) -> bool:
        deleted = self.repository.delete_product(product_id)
        if not deleted:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return True
