from django.urls import path, include
from rest_framework import routers

from api.veiws import TruckViewSet, CargoViewSet


router = routers.DefaultRouter()

router.register('trucks', TruckViewSet)
router.register('cargos', CargoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
