import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

from product.models import Product

DEFAULT_PRODUCTS = [
    {
        "name": "Legacy Product 1",
        "description": "A legacy product that was created before categories existed.",
        "price": 99.99,
        "brand": "Legacy Brand",
        "stock": 10
    },
    {
        "name": "Legacy Product 2",
        "description": "Another legacy product with no assigned category.",
        "price": 59.99,
        "brand": "Legacy Brand",
        "stock": 5
    },
]

def seed_products_without_category():
    for product_data in DEFAULT_PRODUCTS:
        product = Product(**product_data)
        product.save(validate=False) 
        print(f"Product '{product.name}' added without category.")

if __name__ == "__main__":
    seed_products_without_category()
