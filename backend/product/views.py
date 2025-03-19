from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .services import ProductService
from .serializers import ProductSerializer

class ProductCreateView(APIView):    
    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            service = ProductService()
            try:
                product = service.create_product(**serializer.validated_data)
                output_serializer = ProductSerializer(product)
                return Response({'message': 'Product created successfully', 'product': output_serializer.data}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    def get(self, request: Request) -> Response:
        service = ProductService()
        products = service.list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request: Request, product_id: str) -> Response:
        service = ProductService()
        try:
            product = service.get_product_by_id(product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)


class ProductUpdateView(APIView):
    def put(self, request: Request, product_id: str) -> Response:
        service = ProductService()
        try:
            product = service.get_product_by_id(product_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_product = service.update_product(product_id, **serializer.validated_data)
                output_serializer = ProductSerializer(updated_product)
                return Response({'message': 'Product updated successfully', 'product': output_serializer.data}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    def delete(self, request: Request, product_id: str) -> Response:
        service = ProductService()
        try:
            service.delete_product(product_id)
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)
