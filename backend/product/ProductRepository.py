from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from .Product_models import Product
from .Category_models import ProductCategory

class ProductRepository:
    """Handles database interactions for Product"""

    def create_product(self, name: str, description: str, category: ProductCategory, price: float, brand: str, stock: int) -> Product:
        try:
            new_product = Product(
                name=name, 
                description=description, 
                category=category,
                price=price, 
                brand=brand, 
                stock=stock
            )
            new_product.save()
            return new_product
        except ValidationError as e:
            raise e

    def get_all_products(self):
        return Product.objects

    def get_product_by_id(self, product_id: str) -> Product | None:
        try:
            obj_id = ObjectId(product_id)
            return Product.objects.get(id=obj_id)
        except (DoesNotExist, ValidationError):
            return None

    def get_product_by_name(self, name: str) -> Product | None:
        try:
            return Product.objects.get(name=name)
        except DoesNotExist:
            return None

    def delete_product(self, product_id: str) -> bool:
        try:
            obj_id = ObjectId(product_id)
            product = Product.objects.get(id=obj_id)
            product.delete()
            return True
        except (DoesNotExist, ValidationError):
            return False

    def update_product(self, product_id: str, **kwargs) -> Product | None:
        """
        Expects that if the category is being updated, kwargs["category"] is a ProductCategory instance.
        """
        try:
            obj_id = ObjectId(product_id)
            product = Product.objects.get(id=obj_id)
            product.update(**kwargs)
            # Reload to reflect updated values
            product.reload()
            return product
        except (DoesNotExist, ValidationError):
            return None
