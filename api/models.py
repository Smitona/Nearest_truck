import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import PlateAlphaEnd, PlateNumber


class Location(models.Model):
    """Model for locations."""
    city = models.CharField(
        max_length=200,
        blank=False,
    )
    state = models.CharField(
        max_length=200,
        blank=False,
    )
    zip = models.PositiveIntegerField(
        max_length=5,
        unique=True,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    @classmethod
    def get_zip():
        max_pk = Location.objects.latest('pk').pk
        return random.randint(1, max_pk)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ('state',)

    def __str__(self):
        return '{}, {} at {} latitude and {} longitude.'.format(
            self.city, self.state, self.latitude, self.longitude
        )


class Truck(models.Model):
    """Model for trucks."""
    plate_number = models.CharField(
        max_length=5,
        blank=False,
        unique=True,
        validators=[
            PlateAlphaEnd, PlateNumber,
        ],
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='current_loc',
        blank=False,
        to_field='zip',
        default=Location.get_zip,
    )
    cargo_capacity = models.PositiveSmallIntegerField(
        default=20,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
    )

    class Meta:
        verbose_name = 'Truck'
        verbose_name_plural = 'Trucks'
        ordering = ('plate_number',)

    def __str__(self):
        return 'Truck {} with {} cargo capacity currently at {}, {}.'.format(
            self.plate_number, self.cargo_capacity,
            self.location.city, self.location.state,
        )


class Cargo(models.Model):
    """Model for cargos"""
    pickup_loc = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='pickup',
        blank=False,
        to_field='zip',
    )
    delivery_loc = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='deliver',
        blank=False,
        to_field='zip',
    )
    weight = models.PositiveSmallIntegerField(
        default=20,
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
    )
    description = models.TextField(
        blank=False
    )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ('pickup_loc',)

    def __str__(self):
        return 'Cargo {} with total weight {}.'.format(
            self.description[:30], self.weight,
        )

    def formatted_text(self):
        return '<br>'.join(self.description.splitlines())
