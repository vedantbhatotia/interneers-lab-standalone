from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator 

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        min_length=3,
    )
    description = serializers.CharField()
    category = serializers.ChoiceField(
        choices=["Electronics", "Books", "Clothing", "Home"]
    )
    price = serializers.FloatField(validators=[MinValueValidator(0)])
    brand = serializers.CharField(min_length=1)
    stock = serializers.IntegerField(validators=[MinValueValidator(0)])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
