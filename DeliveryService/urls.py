from django.urls import include, path
from rest_framework import routers

from DeliveryService.views import PackageViewSet, PackageCategoryViewSet

delivery_service_router = routers.DefaultRouter()
delivery_service_router.register(r'package', PackageViewSet, basename='packages')
delivery_service_router.register(r'package-categories', PackageCategoryViewSet, basename='package-categories')


urlpatterns = [
    path('api/v1/', include(delivery_service_router.urls)),
]