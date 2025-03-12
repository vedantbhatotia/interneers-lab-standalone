from django.urls import path
from .views import get_products, create_product, get_product, update_product, delete_product

urlpatterns = [
    path('products/', get_products, name='products'),
    path('create-product/', create_product, name='create-product'),
    path('products/<str:id>/', get_product, name='get-product'), 
    path('products/update/<str:id>/', update_product, name='update-product'),
    path('products/delete/<str:id>/', delete_product, name='delete-product'), 
]
