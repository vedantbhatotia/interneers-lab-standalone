from .models import Product
from mongoengine.errors import DoesNotExist, ValidationError

class ProductRepository:
    def create_product(self, name, description, category, price, brand, stock):
        try:
            new_product = Product(name=name, description=description, category=category, price=price, brand=brand, stock=stock)
            new_product.save()
            return new_product
        except ValidationError as e:
            raise e

    def get_all_products(self):
        return list(Product.objects())

    def get_product_by_name(self, name):
        try:
            return Product.objects.get(name=name)
        except (DoesNotExist, ValidationError):
            return None

    def get_product_by_id(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError):
            return None

    def delete_product(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except (DoesNotExist, ValidationError):
            return False

    def update_product(self, product_id, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            product.update(**kwargs)
            product.reload()
            return product
        except (DoesNotExist, ValidationError):
            return None
