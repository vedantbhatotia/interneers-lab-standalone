from django.core.management.base import BaseCommand
from product.models import Product, ProductCategory

DEFAULT_CATEGORY_TITLE = "Uncategorized"
DEFAULT_CATEGORY_DESCRIPTION = "Default category for products with no category."

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
            self.stdout.write(self.style.SUCCESS(f"Created default category '{DEFAULT_CATEGORY_TITLE}'.")) 
        else:
            self.stdout.write(f"Default category '{DEFAULT_CATEGORY_TITLE}' already exists.")


        products_without_category = Product.objects(category=None)
        total = products_without_category.count()

        if total == 0:
            self.stdout.write("No products found without a category.")
            return


        for product in products_without_category:
            product.category = default_category
            product.save()
            self.stdout.write(self.style.SUCCESS(f"Updated product '{product.name}' with default category."))

        self.stdout.write(self.style.SUCCESS(f"Migration complete. {total} products updated."))
