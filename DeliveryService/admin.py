from django.contrib import admin
from DeliveryService.models import Package, PackageCategory

# Register your models here.

admin.site.register(Package)
admin.site.register(PackageCategory)