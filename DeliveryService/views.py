import logging

from django_filters.rest_framework import DjangoFilterBackend

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


from DeliveryService.models import Package, PackageCategory
from DeliveryService.serializers import PackageSerializer, PackageCategorySerializer
from DeliveryService.mixins import SessionManagementMixin
from DeliveryService.filters import PackageFilter
from DeliveryService.tasks import update_delivery_costs



logger = logging.getLogger("main")

class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100



class PackageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet,
                     SessionManagementMixin):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = PackageSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter
    
    def get_queryset(self):
        self.ensure_session(request=self.request)
        queryset = Package.objects.filter(session_id=self.request.session.session_key)
        return queryset
    
    def get_permissions(self):
        if self.action == "except_packages":
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(methods=['get'], detail=False, serializer_class=None, pagination_class=None, filter_backends=None)
    def except_packages(self, request):
        """Run an unscheduled updating delivery costs task."""
        
        return Response({"Message": "Packages sent for cost calculation."}, status=status.HTTP_200_OK)
    

class PackageCategoryViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = PackageCategorySerializer
    pagination_class = DefaultPagination
    queryset = PackageCategory.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = "categories_list"
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)
        cache.set(key=cache_key, value=response, timeout=60 * 5)
        return response
