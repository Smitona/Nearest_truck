
from geopy.distance import geodesic

from api.models import Cargo, Location, Truck


def get_trucks_distance(cargo):
    cargo_pickup = (cargo.pickup_loc.latitude, cargo.pickup_loc.longitude)

    trucks = Truck.objects.all()
    trucks_distance = []

    for truck in trucks:
        truck_location = truck.location.latitude, truck.location.longitude
        distance = geodesic(cargo_pickup, truck_location,).miles

        trucks_distance.append({
                'plate': truck.plate_number,
                'distance': distance
            })

    return trucks_distance


def get_trucks_within_450(cargo):
    cargo_pickup = (cargo.pickup_loc.latitude, cargo.pickup_loc.longitude)
    trucks = Truck.objects.all()
    count = 0

    for truck in trucks:
        truck_location = truck.location.latitude, truck.location.longitude
        distance = geodesic(cargo_pickup, truck_location,).miles

        if distance <= 450:
            count += 1

    return count
