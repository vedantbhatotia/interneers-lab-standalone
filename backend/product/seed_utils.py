import logging
from mongoengine.errors import NotUniqueError
from .Category_models import ProductCategory
from .Product_models import Product

logger = logging.getLogger(__name__)

DEFAULT_CATEGORIES = [
    {"title": "Electronics", "description": "Electronic devices and gadgets"},
    {"title": "Clothing", "description": "Men and women clothing"},
    {"title": "Books", "description": "Books and Literature"},
]

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


def seed_categories():
    for data in DEFAULT_CATEGORIES:
        if not ProductCategory.objects(title=data["title"]).first():
            try:
                ProductCategory(**data).save()
                logger.info(f"Category '{data['title']}' added.")
            except NotUniqueError:
                logger.info(f"Category '{data['title']}' already exists.")


def seed_legacy_products():
    default_category = ProductCategory.objects(title="Electronics").first()
    if not default_category:
        logger.error("Default category 'Electronics' not found. Cannot seed legacy products.")
        return

    for data in DEFAULT_PRODUCTS:
        data["category"] = default_category
        existing = Product.objects(name=data["name"]).first()
        if not existing:
            Product(**data).save()
            logger.info(f"Product '{data['name']}' added.")
        else:
            existing.update(**data)
            logger.info(f"Product '{data['name']}' updated.")
