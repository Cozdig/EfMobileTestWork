from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.permissions import can_view_product, can_create_product, can_edit_product, can_delete_product


class ProductListView(APIView):
    permission_classes = [IsAuthenticated, can_view_product()]

    def get(self, request):
        products = [
            {"id": 1, "name": "Ноутбук", "price": 50000},
            {"id": 2, "name": "Мышь", "price": 1000},
            {"id": 3, "name": "Клавиатура", "price": 3000},
        ]
        return Response({"products": products})


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, can_create_product()]

    def post(self, request):
        return Response(
            {"message": "Товар создан", "product": request.data},
            status=status.HTTP_201_CREATED
        )


class ProductDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), can_view_product()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), can_edit_product()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), can_delete_product()]
        return super().get_permissions()

    def get(self, request, product_id):
        product = {"id": product_id, "name": "Товар", "price": 1000}
        return Response({"product": product})

    def put(self, request, product_id):
        return Response({"message": f"Товар {product_id} обновлен"})

    def delete(self, request, product_id):
        return Response({"message": f"Товар {product_id} удален"})