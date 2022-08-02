from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import products.views as product

router = routers.DefaultRouter()

router.register("product", product.ProductViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/users", product.user),
]
