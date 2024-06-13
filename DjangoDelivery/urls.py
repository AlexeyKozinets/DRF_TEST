from django.contrib import admin
from django.urls import path, include
from DjangoDelivery.yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DeliveryService.urls')),
]

urlpatterns += yasg_urlpatterns
