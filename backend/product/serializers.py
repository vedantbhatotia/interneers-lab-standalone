from rest_framework import serializers
from .models import Product, ProductCategory
from django.core.validators import MinValueValidator 

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(min_length=3)
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    #convert the objectId type to string which can be serialized then 
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the ObjectId to a string
        representation['id'] = str(instance.id)
        return representation



class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=3)
    description = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    price = serializers.FloatField(validators=[MinValueValidator(0)])
    brand = serializers.CharField(min_length=1)
    stock = serializers.IntegerField(validators=[MinValueValidator(0)])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the ObjectId to a string
        representation['id'] = str(instance.id)
        representation['category'] = str(instance.category.id)
        return representation