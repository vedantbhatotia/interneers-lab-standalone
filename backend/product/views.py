from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from .services import ProductService,ProductCategoryService
from .serializers import ProductSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .services import ProductService, ProductCategoryService
from .serializers import ProductSerializer, ProductCategorySerializer

# Product Views
class ProductListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        service = ProductService()
        return service.list_products()

    def perform_create(self, serializer):
        service = ProductService()
        try:
            # The serializer.validated_data["category"] will be a ProductCategory instance,
            # because of the PrimaryKeyRelatedField. If it’s not found, the serializer would already
            # have raised a ValidationError.
            product = service.create_product(**serializer.validated_data)
            serializer.instance = product
        except ValidationError as e:
            raise ValidationError({'error': e.detail})


class ProductRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        service = ProductService()
        return service.list_products()

    def get_object(self):
        service = ProductService()
        product_id = self.kwargs.get('product_id')
        product = service.get_product_by_id(product_id)
        if not product:
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})
        return product

    def perform_update(self, serializer):
        service = ProductService()
        product_id = self.kwargs.get('product_id')

        try:
            updated_product = service.update_product(product_id, **serializer.validated_data)
            serializer.instance = updated_product
        except ValidationError as e:
            raise ValidationError({'error': e.detail})

    def perform_destroy(self, instance):
        service = ProductService()
        product_id = self.kwargs.get('product_id')

        if not service.delete_product(product_id):
            raise ValidationError({"id": f"Product with ID '{product_id}' not found."})



# Category Views
class CategoryListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    def get_queryset(self):
        service = ProductCategoryService()
        return service.list_categories()

    def perform_create(self, serializer):
        service = ProductCategoryService()
        try:
            category = service.create_category(**serializer.validated_data)
            serializer.instance = category
        except ValidationError as e:
            raise ValidationError({'error': e.detail})
        

class CategoryRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCategorySerializer
    lookup_field = 'category_id'

    def get_queryset(self):
        service = ProductCategoryService()
        return service.list_categories()

    def get_object(self):
        service = ProductCategoryService()
        category_id = self.kwargs.get('category_id')
        category = service.get_category_by_id(category_id)
        if not category:
            raise ValidationError({"id": f"Category with ID '{category_id}' not found."})
        return category

    def perform_update(self, serializer):
        service = ProductCategoryService()
        category_id = self.kwargs.get('category_id')

        try:
            updated_category = service.update_category(category_id, **serializer.validated_data)
            serializer.instance = updated_category
        except ValidationError as e:
            raise ValidationError({'error': e.detail})

    def perform_destroy(self, instance):
        service = ProductCategoryService()
        category_id = self.kwargs.get('category_id')

        if not service.delete_category(category_id):
            raise ValidationError({"id": f"Category with ID '{category_id}' not found."})