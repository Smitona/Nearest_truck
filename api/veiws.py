import random

from rest_framework import status, viewsets
from rest_framework.response import Response

from api.models import Cargo, Location, Truck
from api.serializers import (CargoSerializer, ShortCargoSerializer,
                             TruckSerializer)


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def perform_create(self, serializer):
        serializer.save(
           location=Location.get_location(),
        )

    def perform_update(self, serializer):
        location_zip = serializer.validated_data.get('location')
        location_obj = Location.objects.get(zip=location_zip)
        serializer.save(
            location=location_obj
        )


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortCargoSerializer
        return CargoSerializer

    def perform_create(self, serializer):
        pickup_loc_zip = serializer.validated_data.get('pickup_loc')
        delivery_loc_zip = serializer.validated_data.get('delivery_loc')

        pickup_loc = Location.objects.get(zip=pickup_loc_zip)
        delivery_loc = Location.objects.get(zip=delivery_loc_zip)

        serializer.save(
            pickup_loc=pickup_loc,
            delivery_loc=delivery_loc
        )

    def delete(self, pk):
        cargo_exists = Cargo.objects.filter(pk=pk).exists()

        if not cargo_exists:
            return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
        Cargo.objects.get(pk=pk).delete()

        return Response(
                status=status.HTTP_204_NO_CONTENT
            )
