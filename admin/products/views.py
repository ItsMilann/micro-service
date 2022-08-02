import random
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.producer import publish

from .serializers import ProductSerializer
from .models import Product, User


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        publish('product_created', serializer.data)
    
    def perform_update(self, serializer):
        super().perform_update(serializer)
        publish('product_updated', serializer.data)
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        publish("product_deleted", instance.id)

@api_view(["GET"])
def user(request):
    qs = User.objects.all()
    data = random.choice(qs)
    return Response({"user": data.id}, status=200)