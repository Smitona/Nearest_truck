from django.contrib import admin

from api.models import Location, Truck, Cargo


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Location)
class LocationAdmin(BaseAdmin):
    pass


@admin.register(Truck)
class TruckAdmin(BaseAdmin):
    pass


@admin.register(Cargo)
class CargoAdmin(BaseAdmin):
    pass
