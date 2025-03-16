from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    category = serializers.CharField()
    price = serializers.FloatField()
    brand = serializers.CharField()
    stock = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a non-negative value.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a non-negative integer.")
        return value

    def validate_category(self, value):
        allowed_categories = ["Electronics", "Books", "Clothing", "Home"]
        if value not in allowed_categories:
            raise serializers.ValidationError(f"Category must be one of {allowed_categories}.")
        return value

    def validate_brand(self, value):
        if not value:
            raise serializers.ValidationError("Brand cannot be empty.")
        return value
