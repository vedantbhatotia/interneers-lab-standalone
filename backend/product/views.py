from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from .serializers import ProductSerializer, ProductCategorySerializer
from .services import ProductService, ProductCategoryService
from .mongo_filter_backend import MongoCustomFilter

class ProductListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [MongoCustomFilter,filters.OrderingFilter]  
    ordering_fields = ['price', 'stock', 'created_at']
    ordering = ['created_at']  
    def get_queryset(self):
        service = ProductService()
        return service.list_products()

    def perform_create(self, serializer):
        service = ProductService()
        try:
            # The serializer.validated_data["category"] will be a ProductCategory instance.
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


class CategoryListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    # pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]    

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
    filter_backends = [filters.OrderingFilter]

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
