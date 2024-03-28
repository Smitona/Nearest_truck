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


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def get_serializer_class(self):
        if self.request.action == 'list':
            return ShortCargoSerializer
        return CargoSerializer

    def get_queryset(self):
        cargos = Cargo.objects.all()

        if self.request.action == 'list':
            return cargos.annotate(
                trucks_count=Count(
                    self.get_trucks_distance()['distance'] <= 451
                )
            )

        return cargos.annotate(
            trucks_distance=self.get_trucks_distance()
        )

    def get_distance(self, pickup, truck_location):
        pickup_location = Location.objects.get(zip=pickup)
        truck_location = Location.objects.get(zip=truck_location)
        distance = geodesic(
            (pickup_location.latitude, pickup_location.longitude),
            (truck_location.latitude, truck_location.longitude)
        ).miles

        return distance

    def get_trucks_distance(self):
        trucks = Truck.objects.all()
        cargos = Cargo.objects.all()

        trucks_distance = []
        for cargo in cargos:
            for truck in trucks:
                distance = self.get_distance(cargo.pickup, truck.current_loc)
                trucks_distance.append({
                    'plate': truck.plate_number,
                    'distance': distance
                })
                return trucks_distance

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
