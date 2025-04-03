from .base_model import TimeStampedDocument
import mongoengine

class ProductCategory(TimeStampedDocument):
    title = mongoengine.StringField(required=True, unique=True)
    description = mongoengine.StringField(required=True)
    meta = {'collection': 'product_categories'}
    
    def __str__(self):
        return self.title