from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from .Category_models import ProductCategory

class ProductCategoryRepository:
    """Handles database interactions for ProductCategory"""
    def create_category(self, title: str, description: str) -> ProductCategory:
        try:
            new_category = ProductCategory(title=title, description=description)
            new_category.save()
            return new_category
        except ValidationError as e:
            raise e 
        
    def get_all_categories(self):
        return ProductCategory.objects.all()

    def get_category_by_id(self, category_id: str) -> ProductCategory | None:
        try:
            obj_id = ObjectId(category_id)
            return ProductCategory.objects.get(id=obj_id)
        except (DoesNotExist, ValidationError):
            return None
        
    def get_category_by_name(self, category_name: str) -> ProductCategory | None:
        try:
            return ProductCategory.objects.get(title=category_name)
        except (DoesNotExist, ValidationError):
            return None
        
    def update_category(self, category_id: str, **kwargs) -> ProductCategory | None:
        try:
            obj_id = ObjectId(category_id)
            category = ProductCategory.objects.get(id=obj_id)
            if category:
                category.update(**kwargs)
                category.reload()
                return category
            return None
        except (DoesNotExist, ValidationError):
            return None
        
    def delete_category(self, category_id: str) -> bool:
        try:
            obj_id = ObjectId(category_id)
            category = ProductCategory.objects.get(id=obj_id)
            if category:
                category.delete()
                return True
            return False
        except (DoesNotExist, ValidationError):
            return False
