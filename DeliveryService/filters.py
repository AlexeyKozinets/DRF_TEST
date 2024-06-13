from django_filters import rest_framework as filters
from DeliveryService.models import Package

class PackageFilter(filters.FilterSet):
    category_id = filters.NumberFilter(field_name='category')
    has_delivery_cost = filters.BooleanFilter(field_name='delivery_cost', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Package
        fields = ['category_id', 'has_delivery_cost']

