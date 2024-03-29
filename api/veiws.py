import random
from django.db.models import Count

from rest_framework import viewsets, status
from rest_framework.response import Response

from geopy.distance import geodesic

from api.models import Location, Truck, Cargo
from api.serializers import (CargoSerializer, TruckSerializer,
                             ShortCargoSerializer)


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def get_location(obj):
        max_pk = Location.objects.latest('pk').pk
        location_pk = random.randint(1, max_pk)
        location = Location.objects.get(pk=location_pk)
        return location

    def perform_create(self, serializer):
        serializer.save(
           location=self.get_location(),
        )


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortCargoSerializer
        return CargoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        pickup_loc_zip = serializer.validated_data.get('pickup_loc')
        delivery_loc_zip = serializer.validated_data.get('delivery_loc')

        pickup_loc = Location.objects.get(zip=pickup_loc_zip)
        delivery_loc = Location.objects.get(zip=delivery_loc_zip)

        cargo = Cargo.objects.create(
            description=serializer.validated_data.get('description'),
            weight=serializer.validated_data.get('weight'),
            pickup_loc=pickup_loc,
            delivery_loc=delivery_loc
        )

        return Response(
                ShortCargoSerializer(cargo).data,
                status=status.HTTP_201_CREATED
            )

    def delete(self, request, pk):
        cargo_exists = Cargo.objects.filter(pk=pk).exists()

        if not cargo_exists:
            return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
        Cargo.objects.get(pk=pk).delete()

        return Response(
                status=status.HTTP_204_NO_CONTENT
            )
