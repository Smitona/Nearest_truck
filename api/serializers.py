from django.db import transaction
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
    location = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = Truck
        fields = (
            'plate_number',
            'location',
            'cargo_capacity',
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.location = 'description', instance.description
        return super().update(instance, validated_data)


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

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get(
            'description', instance.description
        )
        return super().update(instance, validated_data)


class ShortCargoSerializer(serializers.ModelSerializer):
    trucks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cargo
        fields = (
            'pickup_loc',
            'delivery_loc',
            'trucks_count'
        )
