from .base_model import TimeStampedDocument
from .Category_models import ProductCategory
import mongoengine

class Product(TimeStampedDocument):
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    category = mongoengine.ReferenceField(
        ProductCategory, required=True, reverse_delete_rule=mongoengine.CASCADE
    )
    price = mongoengine.FloatField(required=True, min_value=0)
    brand = mongoengine.StringField(required=True)
    stock = mongoengine.IntField(required=True, min_value=0)
    meta = {'collection': 'products'}
    
    def __str__(self):
        return self.name