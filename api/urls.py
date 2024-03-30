from django.urls import include, path
from rest_framework import routers

from api.veiws import CargoViewSet, TruckViewSet

router = routers.DefaultRouter()

router.register('trucks', TruckViewSet)
router.register('cargos', CargoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
