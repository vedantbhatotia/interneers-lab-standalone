from rest_framework import serializers
from django.core.validators import MinValueValidator
from .Product_models import Product
from .Category_models import  ProductCategory

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(min_length=3)
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # Convert the ObjectId to a string for proper JSON serialization.
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id)
        return representation

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=3)
    description = serializers.CharField()
    # Used for writing/updating the product
    category = serializers.CharField(write_only=True)
    price = serializers.FloatField(validators=[MinValueValidator(0)])
    # For output, return the full nested category object.
    category_object = ProductCategorySerializer(source='category',read_only=True)
    brand = serializers.CharField(min_length=1)
    stock = serializers.IntegerField(validators=[MinValueValidator(0)])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = str(instance.category)
        representation['id'] = str(instance.id)
        if representation.get('category_object'):
            representation['category_object']['id'] = str(instance.category.id)
        return representation
