from django.urls import path
from .views import ProductCreateView, ProductListView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/update/<str:name>/', ProductUpdateView.as_view(), name='product-update'),
    path('products/delete/<str:name>/', ProductDeleteView.as_view(), name='product-delete'),
]
