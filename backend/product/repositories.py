from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from .models import Product, ProductCategory

class ProductCategoryRepository:
    """Handles database interactions for ProductCategory"""
    def create_category(self, title: str, description: str) -> ProductCategory:
        try:
            new_category = ProductCategory(title=title, description=description)
            new_category.save()
            return new_category
        except ValidationError as e:
            raise e 
        
    def get_all_categories(self):
        return ProductCategory.objects.all()

    def get_category_by_id(self, category_id: str) -> ProductCategory | None:
        try:
            obj_id = ObjectId(category_id)
            return ProductCategory.objects.get(id=obj_id)
        except (DoesNotExist, ValidationError) as e:
            return None
        
    def get_category_by_name(self, category_name: str) -> ProductCategory | None:
        try:
            return ProductCategory.objects.get(title=category_name)
        except (DoesNotExist, ValidationError) as e:
            return None
        
    def update_category(self, category_id: str, **kwargs) -> ProductCategory | None:
        try:
            obj_id = ObjectId(category_id)
            category = ProductCategory.objects.get(id=obj_id)
            if category:
                category.update(**kwargs)
                category.reload()
                return category
            return None
        except (DoesNotExist, ValidationError) as e:
            return None
        
    def delete_category(self, category_id: str) -> bool:
        try:
            obj_id = ObjectId(category_id)
            category = ProductCategory.objects.get(id=obj_id)
            if category:
                category.delete()
                return True
            return False
        except (DoesNotExist, ValidationError) as e:
            return False

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
