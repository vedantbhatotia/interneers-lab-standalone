# product/tests/test_seed_utils.py
from product.Category_models import ProductCategory
from product.Product_models import Product

TEST_CATEGORIES = [
    {"title": "TestCat1", "description": "Test category 1"},
    {"title": "TestCat2", "description": "Test category 2"},
]

TEST_PRODUCTS = [
    {
        "name": "Test Product 1",
        "description": "Test product 1 desc",
        "price": 10.99,
        "brand": "Test Brand",
        "stock": 50,
    }
]


def reseed_test_data():
    Product.drop_collection()
    ProductCategory.drop_collection()

    category_objs = []
    for cat in TEST_CATEGORIES:
        category_objs.append(ProductCategory(**cat).save())

    for prod in TEST_PRODUCTS:
        prod["category"] = category_objs[0]
        Product(**prod).save()

    print ("seeded data for tests")
