# from rest_framework.exceptions import ValidationError
# from .ProductRepository import ProductRepository
# from .ProductCategoryRepository import ProductCategoryRepository
# from .Product_models import Product
# from .Category_models import ProductCategory
# from django.db.models.query import QuerySet
# from django.db import transaction


# class ProductService:
#     def __init__(self):
#         self.repository = ProductRepository()
#         self.category_repository = ProductCategoryRepository()

#     def create_product(self, name: str, description: str, category, price: float, brand: str, stock: int) -> Product:
#         if self.repository.get_product_by_name(name):
#             raise ValidationError({"name": "Product already exists"})

#         # Ensure the category is a ProductCategory instance.
#         if not isinstance(category, ProductCategory):
#             # Lookup by id using the repository.
#             category_obj = self.category_repository.get_category_by_id(category)
#             if not category_obj:
#                 raise ValidationError({"category": f"Category with id '{category}' not found."})
#         else:
#             category_obj = category

#         return self.repository.create_product(name, description, category_obj, price, brand, stock)

    
#     def get_product_by_id(self, product_id: str) -> Product:
#         product = self.repository.get_product_by_id(product_id)
#         if not product:
#             raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
#         return product

#     def list_products(self) -> QuerySet:
#         return self.repository.get_all_products()

#     def update_product(self, product_id: str, **kwargs) -> Product:
#         if not kwargs:
#             raise ValidationError({"error": "No update fields provided."})
        
#         with transaction.atomic():
#             if "category" in kwargs:
#                 category = self.category_repository.get_category_by_id(kwargs["category"])
#                 if not category:
#                     raise ValidationError({"category": f"Category with ID '{kwargs['category']}' not found."})
#                 kwargs["category"] = category

#             updated = self.repository.update_product(product_id, **kwargs)
#             if not updated:
#                 raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
#             return updated

#     def delete_product(self, product_id: str) -> bool:
#         deleted = self.repository.delete_product(product_id)
#         if not deleted:
#             raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
#         return True


from rest_framework.exceptions import ValidationError
from .ProductRepository import ProductRepository
from .ProductCategoryRepository import ProductCategoryRepository
from .Product_models import Product
from .Category_models import ProductCategory

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.category_repository = ProductCategoryRepository()

    def create_product(self, name: str, description: str, category, price: float, brand: str, stock: int) -> Product:
        if self.repository.get_product_by_name(name):
            raise ValidationError({"name": "Product already exists"})

        if not isinstance(category, ProductCategory):
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

    def list_products(self):
        return self.repository.get_all_products()

    def update_product(self, product_id: str, **kwargs) -> Product:
        if not kwargs:
            raise ValidationError({"error": "No update fields provided."})

        try:
            with Product._get_collection().database.client().start_session() as session:
                with session.start_transaction():
                    if "category" in kwargs:
                        category = self.category_repository.get_category_by_id(kwargs["category"])
                        if not category:
                            raise ValidationError({"category": f"Category with ID '{kwargs['category']}' not found."})
                        kwargs["category"] = category

                    updated = self.repository.update_product(product_id, **kwargs)
                    if not updated:
                        raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
                    return updated
        except Exception as e:
            raise ValidationError({"error": str(e)})

    def delete_product(self, product_id: str) -> bool:
        deleted = self.repository.delete_product(product_id)
        if not deleted:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return True
