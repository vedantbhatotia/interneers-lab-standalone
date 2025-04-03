from django.apps import AppConfig
from django.db.utils import OperationalError
from mongoengine.errors import NotUniqueError
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        """Seed Categories and Legacy Products when the app is ready"""
        from .Category_models import ProductCategory
        from .Product_models import Product  

        DEFAULT_CATEGORIES = [
            {"title": "Electronics", "description": "Electronic devices and gadgets"},
            {"title": "Clothing", "description": "Men and women clothing"},
            {"title": "Books", "description": "Books and Literature"},
        ]

        try:
            for category_data in DEFAULT_CATEGORIES:
                title = category_data["title"]
                category = ProductCategory.objects(title=title).first()
                if not category:
                    ProductCategory(**category_data).save()
                    logger.info(f"Category '{title}' added.")
                else:
                    logger.info(f"Category '{title}' already exists.")
        except (OperationalError, ImproperlyConfigured, NotUniqueError) as e:
            logger.error(f"Error during category seeding: {e}")


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

        try:
            for product_data in DEFAULT_PRODUCTS:
                existing_product = Product.objects(name=product_data["name"]).first()
                if existing_product:
                    existing_product.update(**product_data)  # MongoEngine equivalent of update_or_create
                    logger.info(f"Product '{product_data['name']}' updated.")
                else:
                    Product(**product_data).save()
                    logger.info(f"Product '{product_data['name']}' added without category.")
        except (OperationalError, ImproperlyConfigured, NotUniqueError) as e:
            logger.error(f"Error during seeding legacy products: {e}")
