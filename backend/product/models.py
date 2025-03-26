import mongoengine
from datetime import datetime, timezone

class ProductCategory(mongoengine.Document):
    title = mongoengine.StringField(required=True, unique=True)
    description = mongoengine.StringField(required=True)
    created_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'product_categories'}

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title  




class Product(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    category = mongoengine.ReferenceField(
        ProductCategory, required=True, reverse_delete_rule=mongoengine.CASCADE
    )
    price = mongoengine.FloatField(required=True, min_value=0)
    brand = mongoengine.StringField(required=True)
    stock = mongoengine.IntField(required=True, min_value=0)
    created_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    meta = {'collection': 'products'}
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.name 
