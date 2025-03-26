from rest_framework import serializers
from .models import Product,ProductCategory
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator 


class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(
        min_length=3,
        validators=[UniqueValidator(queryset=ProductCategory.objects.all())]
    )
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)



class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=3)
    description = serializers.CharField()
    category = serializers.SlugRelatedField(
        slug_field="title", queryset=ProductCategory.objects.all()
    )
    price = serializers.FloatField(validators=[MinValueValidator(0)])
    brand = serializers.CharField(min_length=1)
    stock = serializers.IntegerField(validators=[MinValueValidator(0)])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
