import mongoengine
from datetime import datetime
class Product(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    category = mongoengine.StringField(required=True)
    price = mongoengine.IntField(required=True)
    brand = mongoengine.StringField(required=True)
    stock = mongoengine.IntField(required=True)
    created_at = mongoengine.DateTimeField(default=datetime.now)
    updated_at = mongoengine.DateTimeField(default=datetime.now)
    meta = {
        'collection': 'products' # maps this model to the 'products' collection in MongoDB
    }
    def save(self,*args,**kwargs):
        self.updated_at = datetime.utcnow()
        return super(Product, self).save(*args, **kwargs) #calls the original MongoEngine .save() method.