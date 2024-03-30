from django.db import transaction
from rest_framework import serializers

from api.models import Cargo, Location, Truck
from api.utils import get_trucks_distance, get_trucks_within_450
from api.validators import validate_plate_alpha_end, validate_plate_number


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = (
            'zip',
            'city',
            'state',
            'latitude',
            'longitude',
        )


class TruckSerializer(serializers.ModelSerializer):
    location = serializers.CharField()
    plate_number = serializers.CharField(
        max_length=5, required=True,
        validators=[
            validate_plate_number, validate_plate_alpha_end
        ]
    )
    cargo_capacity = serializers.CharField(required=True)

    class Meta:
        model = Truck
        fields = (
            'id',
            'plate_number',
            'location',
            'cargo_capacity',
        )

    def validate(self, data):
        if not validate_plate_number(data['plate_number']):
            raise serializers.ValidationError(
                'Plate starts with number from 1000 to 9999 before the letter.'
            )
        if not validate_plate_alpha_end(data['plate_number']):
            raise serializers.ValidationError(
                'Plate must have an uppercase letter at the end.'
            )

        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['location'] = LocationSerializer(instance.location).data
        return data


class CargoSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=200)
    pickup_loc = serializers.CharField(max_length=5)
    delivery_loc = serializers.CharField(max_length=5)
    trucks = serializers.SerializerMethodField()

    def get_trucks(self, obj):
        return get_trucks_distance(obj)

    class Meta:
        model = Cargo
        fields = (
            'description',
            'weight',
            'pickup_loc',
            'delivery_loc',
            'trucks'
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get(
            'description', instance.description
        )
        return super().update(instance, validated_data)


class ShortCargoSerializer(serializers.ModelSerializer):
    trucks_count = serializers.SerializerMethodField()
    pickup_loc = LocationSerializer()
    delivery_loc = LocationSerializer()

    class Meta:
        model = Cargo
        fields = (
            'id',
            'description',
            'weight',
            'pickup_loc',
            'delivery_loc',
            'trucks_count'
        )

    def get_trucks_count(self, obj):
        return get_trucks_within_450(obj)
