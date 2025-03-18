from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<str:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'), 
    path('products/update/<str:product_id>/', ProductUpdateView.as_view(), name='product-update'), 
    path('products/delete/<str:product_id>/', ProductDeleteView.as_view(), name='product-delete'),
]
