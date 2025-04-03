import logging
from django.core.management.base import BaseCommand
from product.Product_models import Product
from product.Category_models import ProductCategory

DEFAULT_CATEGORY_TITLE = "Uncategorized"
DEFAULT_CATEGORY_DESCRIPTION = "Default category for products with no category."

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Migrate existing products missing a product category by assigning them a default category."

    def handle(self, *args, **options):
        default_category = ProductCategory.objects(title=DEFAULT_CATEGORY_TITLE).first()
        if not default_category:
            default_category = ProductCategory(
                title=DEFAULT_CATEGORY_TITLE,
                description=DEFAULT_CATEGORY_DESCRIPTION
            )
            default_category.save()
            logger.info(f"Created default category '{DEFAULT_CATEGORY_TITLE}'.")
        else:
           logger.info(f"Default category '{DEFAULT_CATEGORY_TITLE}' already exists.")


        products_without_category = Product.objects(category=None)
        total = products_without_category.count()

        if total == 0:
            logger.info("No Products without a category found")
            return


        for product in products_without_category:
            product.category = default_category
            product.save()
            logger.info(f"Updated product '{product.name}' with default category.")

        logger.info(f"Migration complete. {total} products updated.")