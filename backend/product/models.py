import mongoengine
from datetime import datetime, timezone

class Product(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    category = mongoengine.StringField(required=True)
    price = mongoengine.IntField(required=True)
    brand = mongoengine.StringField(required=True)
    stock = mongoengine.IntField(required=True)
    created_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = mongoengine.DateTimeField(default=lambda: datetime.now(timezone.utc))
    
    meta = {
        'collection': 'products'  # maps this model to the 'products' collection in MongoDB
    }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super(Product, self).save(*args, **kwargs)
