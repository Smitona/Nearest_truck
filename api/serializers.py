from rest_framework import serializers

from api.models import Location, Truck, Cargo


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'zip'
            'city',
            'state',
            'latitude',
            'longitude',
        )


class TruckSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Truck
        fields = (
            'plate_number',
            'location',
            'cargo_capacity',
        )


class CargoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    pickup_loc = LocationSerializer(many=False, read_only=True)
    delivery_loc = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = Cargo
        fields = (
            'description',
            'weight'
            'pickup_loc',
            'delivery_loc',
        )

    @staticmethod
    def get_description(obj):
        return obj.formatted_text()
