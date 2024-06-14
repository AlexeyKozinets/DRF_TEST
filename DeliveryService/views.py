import logging

from django_filters.rest_framework import DjangoFilterBackend

from django.core.cache import cache

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


from DeliveryService.models import Package, PackageCategory
from DeliveryService.serializers import PackageSerializer, PackageCategorySerializer
from DeliveryService.mixins import SessionManagementMixin, CacheManagementMixin
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
                     SessionManagementMixin,
                     CacheManagementMixin):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = PackageSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter

    def initial(self, request, *args, **kwargs):
        if self.action in ["create", "accept_packages"]:
            cache_key = f'package_list_for_{self.request.session.session_key}'
            cache.delete(cache_key)
        return super().initial(request, *args, **kwargs)
    
    def get_queryset(self):
        self.ensure_session(request=self.request)
        queryset = self.cache_or_select(
            response_data=Package.objects.filter(session_id=self.request.session.session_key),
            cache_key=f"package_list_for_{self.request.session.session_key}"
            )
        return queryset
    
    def get_permissions(self):
        if self.action == "accept_packages":
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(methods=['get'], detail=False, serializer_class=None, pagination_class=None, filter_backends=None)
    def accept_packages(self, request):
        """Run an unscheduled updating delivery costs task."""

        update_delivery_costs.delay()
        return Response({"Message": "Packages sent for cost calculation."}, status=status.HTTP_200_OK)
    

class PackageCategoryViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = PackageCategorySerializer
    pagination_class = DefaultPagination
 

    def get_queryset(self):
        queryset =  self.cache_or_select(
            response_data=PackageCategory.objects.all(),
            cache_key=f"pacage_categories"
            )
        return queryset
