import logging

from rest_framework import serializers

from DeliveryService.models import Package, PackageCategory
from DeliveryService.mixins import SessionManagementMixin


logger = logging.getLogger("main")


class PackageSerializer(serializers.ModelSerializer, SessionManagementMixin):

    delivery_cost = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = ["id", "category", "name", "weight", "price", "delivery_cost"]
        extra_kwargs = {"delivery_cost": {"read_only": True}}

    def get_delivery_cost(self, obj):
        return obj.delivery_cost if obj.delivery_cost is not None else "Не рассчитано"

    def validate(self, attrs):

        request = self.context['request']
        self.ensure_session(request=request)
        attrs["session_id"] = request.session.session_key

        return attrs
    
class PackageCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageCategory
        fields = "__all__"
