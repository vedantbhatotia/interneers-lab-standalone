from rest_framework.exceptions import ValidationError
from .repositories import ProductRepository
from .models import Product

class ProductCategoryService:
    def __init__(self):
        self.repository = ProductRepository()

    





class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, name: str, description: str, category: str, price: float, brand: str, stock: int) -> Product:
        existing = self.repository.get_product_by_name(name)
        if existing:
            raise ValidationError({"name": "Product already exists"})
        return self.repository.create_product(name, description, category, price, brand, stock)

    def get_product_by_id(self, product_id: str) -> Product:
        product = self.repository.get_product_by_id(product_id)
        if not product:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return product

    def list_products(self) -> list[Product]:
        return self.repository.get_all_products()

    def update_product(self, product_id: str, **kwargs) -> Product:
        if not kwargs:
            raise ValidationError({"error": "No update fields provided."})

        updated = self.repository.update_product(product_id, **kwargs)
        if not updated:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return updated


    def delete_product(self, product_id: str) -> bool:
        deleted = self.repository.delete_product(product_id)
        if not deleted:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return True
