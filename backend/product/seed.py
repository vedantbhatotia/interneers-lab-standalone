import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")

django.setup()

from product.models import ProductCategory

DEFAULT_CATEGORIES = [
    {"title": "Electronics", "description": "Electronic devices and gadgets"},
    {"title": "Clothing", "description": "Men and women clothing"},
    {"title": "Books", "description": "Books and Literature"},
]

def seed_categories():
    for category_data in DEFAULT_CATEGORIES:
        title = category_data["title"]
        if not ProductCategory.objects(title=title):
            ProductCategory(**category_data).save()
            print(f"Category '{title}' added.")
        else:
            print(f"Category '{title}' already exists.")

if __name__ == "__main__":
    seed_categories()

# this script would be executed everytime the seed.py is called not everytime the server starts