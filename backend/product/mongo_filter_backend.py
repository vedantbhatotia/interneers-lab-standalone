from rest_framework.filters import BaseFilterBackend
from mongoengine.queryset.visitor import Q
from datetime import datetime

class MongoCustomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}
        search_term = request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) | Q(description__icontains=search_term) | Q(brand__icontains=search_term)
            )
        
        brand = request.query_params.get('brand')
        if brand:
            # queryset = queryset.filter(brand__iexact=brand)
            filters['brand__iexact'] = brand
        
        category = request.query_params.get('category')
        if category:
            # queryset = queryset.filter(category=category)
            filters['category'] = category

        price_min = request.query_params.get('price_min')
        if price_min is not None:
            try:
                price_min = float(price_min)
                # queryset = queryset.filter(price__gte=price_min)
                filters['price__gte'] = price_min
            except ValueError:
                pass 

        price_max = request.query_params.get('price_max')
        if price_max is not None:
            try:
                price_max = float(price_max)
                # queryset = queryset.filter(price__lte=price_max)
                filters['price__lte'] = price_max
            except ValueError:
                pass 

        stock_min = request.query_params.get('stock_min')
        if stock_min is not None:
            try:
                stock_min = int(stock_min)
                # queryset = queryset.filter(stock__gte=stock_min)
                filters['stock__gte'] = stock_min
            except ValueError:
                pass
        
        stock_max = request.query_params.get('stock_max')
        if stock_max is not None:
            try:
                stock_max = int(stock_max)
                filters['stock__lte'] = stock_max
                # queryset = queryset.filter(stock__lte=stock_max)
            except ValueError:
                pass
        
        if filters:
            queryset = queryset.filter(**filters)

        return queryset