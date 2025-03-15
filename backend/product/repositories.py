# repositories layer --> handles the data access and manipulation for product data
# interacts with the database
from .models import Product
from mongoengine.errors import DoesNotExist, ValidationError
class ProductRepository:
     #self refers to the instance of the productRepository class and is used to access the instance variables and methods of the class.
    def create_product(name, description, category, price, brand, stock):
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
            return {"error": str(e)} 
        
    def get_all_products():
        return list(Product.objects()) 

    def get_product_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError):
            return None 

    def delete_product(product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except (DoesNotExist, ValidationError):
            return False
        
    def update_product(self, id, **kwargs):
        #allows passing any number of named arguments(kwargs) dynamically to the update_product method
        try:
            product = Product.objects.get(id=id)
            product.update(**kwargs) 
            return True
        except Product.DoesNotExist:
            return False
