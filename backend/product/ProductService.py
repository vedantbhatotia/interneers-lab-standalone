from rest_framework.exceptions import ValidationError,NotFound
from .ProductRepository import ProductRepository
from .ProductCategoryRepository import ProductCategoryRepository
from .Product_models import Product
from .Category_models import ProductCategory
from typing import Union


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.category_repository = ProductCategoryRepository()

    def create_product(self, name: str, description: str, category: Union[str, ProductCategory], price: float, brand: str, stock: int) -> Product:
        if self.repository.get_product_by_name(name):
            raise ValidationError(detail={"name": "Product already exists"})

        if not isinstance(category, ProductCategory):
            category_obj = self.category_repository.get_category_by_id(category)
            if not category_obj:
                raise ValidationError(detail={"category": f"Category with ID '{category}' not found."})
        else:
            category_obj = category

        return self.repository.create_product(name, description, category_obj, price, brand, stock)

    def get_product_by_id(self, product_id: str) -> Product:
        product = self.repository.get_product_by_id(product_id)
        if not product:
            raise NotFound(detail={"error": f"Product with ID '{product_id}' not found."})
        return product

    def list_products(self):
        return self.repository.get_all_products()
    
    def update_product(self, product_id: str, **kwargs) -> Product:
        if not kwargs:
            raise ValidationError(detail={"error": "No update fields provided."})

        if "category" in kwargs:
            category = self.category_repository.get_category_by_id(kwargs["category"])
            if not category:
                raise ValidationError(detail={"category": f"Category with ID '{kwargs['category']}' not found."})
            kwargs["category"] = category

        try:
            with Product._get_collection().database.client.start_session() as session:
                with session.start_transaction():
                    updated = self.repository.update_product(product_id, **kwargs)
                    if not updated:
                        raise ValidationError(detail={"error": f"Product with ID '{product_id}' not found."})
                    return updated

        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(detail={"error": str(e)})


    def delete_product(self, product_id: str) -> bool:
        deleted = self.repository.delete_product(product_id)
        if not deleted:
            raise ValidationError(detail={"error": f"Product with ID '{product_id}' not found."})
        return True
