from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4  
PRODUCTS = {}  

@api_view(['POST'])
def create_product(request):
    data = request.data
    required_fields = ['name', 'description', 'category', 'price', 'brand', 'quantity']
    for field in required_fields:
        if field not in data:
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
        if str(data[field]) == '': 
            return Response({'error': f'{field} cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        price = int(data['price'])
        if price <= 0:
            return Response({'error': 'price must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'price must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        quantity = int(data['quantity'])
        if quantity < 0:
            return Response({'error': 'quantity cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'quantity must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)

    product_id = str(uuid4())
    PRODUCTS[product_id] = {
        "id": product_id,
        "name": data['name'],
        "description": data['description'],
        "category": data['category'],
        "price": price,
        "brand": data['brand'],
        "quantity": quantity
    }

    print(f"Product added: {PRODUCTS}") 
    return Response(PRODUCTS[product_id], status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_products(request):
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            return Response({"error": "Page must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"error": "Page must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

    limit = 4
    products_list = list(PRODUCTS.values())
    total_products = len(products_list)

    if total_products == 0:
        return Response({"error": "No products available", "products": []}, status=status.HTTP_200_OK)

    total_pages = (total_products // limit) + (1 if total_products % limit > 0 else 0)
    start = (page - 1) * limit
    end = min(total_products, start + limit) 

    if start >= total_products:
        return Response({
            "error": "No products available for this page",
            "products": []
        }, status=status.HTTP_200_OK)

    paginated_products = products_list[start:end]

    return Response({
        "total_products": total_products,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "products": paginated_products
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product(request, id):
    product = PRODUCTS.get(id)
    if not product:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(product, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_product(request, id):
    product = PRODUCTS.get(id)
    if not product:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    allowed_fields = ['name', 'description', 'category', 'price', 'brand', 'quantity']

    for field in allowed_fields:
        if field in data:
            if field == 'price':
                try:
                    price = int(data['price'])
                    if price <= 0:
                        return Response({'error': 'price must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)
                    product['price'] = price
                except ValueError:
                    return Response({'error': 'price must be a valid number'}, status=status.HTTP_400_BAD_REQUEST)
            elif field == 'quantity':
                try:
                    quantity = int(data['quantity'])
                    if quantity < 0:
                        return Response({'error': 'quantity cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
                    product['quantity'] = quantity
                except ValueError:
                    return Response({'error': 'quantity must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                product[field] = data[field]

    PRODUCTS[id] = product
    return Response(product, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_product(request, id):
    if id not in PRODUCTS:  
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    del PRODUCTS[id]
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)

