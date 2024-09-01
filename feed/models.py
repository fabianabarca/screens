from django.contrib.gis.db import models

# Create your models here.


class InfoProvider(models.Model):
    name = models.CharField(
        max_length=255, help_text="Nombre del proveedor de información."
    )
    api_url = models.URLField(
        help_text="URL base de la API del proveedor de información."
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Indica si este proveedor de información está activo. Solamente un proveedor puede estar activo a la vez.",
    )

    def save(self, *args, **kwargs):
        if self.is_active:
            InfoProvider.objects.filter(is_active=True).update(is_active=False)
        super(InfoProvider, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Stop(models.Model):
    """Individual locations where vehicles pick up or drop off riders.
    Maps to stops.txt in the GTFS feed.
    """

    stop_id = models.CharField(
        max_length=255, primary_key=True, help_text="Identificador único de la parada."
    )
    stop_code = models.CharField(
        max_length=255, blank=True, null=True, help_text="Código de la parada."
    )
    stop_name = models.CharField(max_length=255, help_text="Nombre de la parada.")
    stop_desc = models.TextField(
        blank=True, null=True, help_text="Descripción de la parada."
    )
    stop_point = models.PointField(
        blank=True, null=True, help_text="Punto georreferenciado de la parada."
    )
    zone_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Identificador de la zona."
    )
    stop_url = models.URLField(blank=True, null=True, help_text="URL de la parada.")
    location_type = models.PositiveIntegerField(
        blank=True, null=True, help_text="Tipo de parada."
    )
    parent_station = models.CharField(
        max_length=255, blank=True, help_text="Estación principal."
    )
    wheelchair_boarding = models.PositiveIntegerField(
        blank=True, null=True, help_text="Acceso para sillas de ruedas."
    )

    def __str__(self):
        return self.stop_name


class Station(models.Model):
    """A group of related stops where vehicles pick up or drop off riders.
    Maps to stops.txt in the GTFS feed.
    """

    station_id = models.CharField(
        max_length=255,
        primary_key=True,
        help_text="Identificador único de la estación.",
    )
    station_name = models.CharField(max_length=255, help_text="Nombre de la estación.")
    station_desc = models.TextField(
        blank=True, null=True, help_text="Descripción de la estación."
    )
    station_point = models.PointField(
        blank=True, null=True, help_text="Punto georreferenciado de la estación."
    )
    zone_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Identificador de la zona."
    )
    station_url = models.URLField(
        blank=True, null=True, help_text="URL de la estación."
    )
    location_type = models.PositiveIntegerField(
        blank=True, null=True, help_text="Tipo de estación."
    )
    parent_station = models.CharField(
        max_length=255, blank=True, help_text="Estación principal."
    )
    wheelchair_boarding = models.PositiveIntegerField(
        blank=True, null=True, help_text="Acceso para sillas de ruedas."
    )

    def __str__(self):
        return self.station_name


class Vehicle(models.Model):
    """Vehicles that are used for public transit.
    Maps to vehicles.txt in the GTFS feed.
    """

    vehicle_id = models.CharField(
        max_length=255, primary_key=True, help_text="Identificador único del vehículo."
    )
    vehicle_label = models.CharField(
        max_length=255, blank=True, null=True, help_text="Etiqueta del vehículo."
    )
    vehicle_license_plate = models.CharField(
        max_length=255, blank=True, null=True, help_text="Placa del vehículo."
    )
    vehicle_model = models.CharField(
        max_length=255, blank=True, null=True, help_text="Modelo del vehículo."
    )
    vehicle_make = models.CharField(
        max_length=255, blank=True, null=True, help_text="Marca del vehículo."
    )
    vehicle_year = models.PositiveIntegerField(
        blank=True, null=True, help_text="Año del vehículo."
    )
    vehicle_url = models.URLField(blank=True, null=True, help_text="URL del vehículo.")
    wheelchair_accessible = models.PositiveIntegerField(
        blank=True, null=True, help_text="Acceso para sillas de ruedas."
    )

    def __str__(self):
        return self.vehicle_label


class Screen(models.Model):
    ORIENTATION_CHOICES = [
        ("landscape", "Horizontal"),
        ("portrait", "Vertical"),
    ]
    RATIO_CHOICES = [
        ("4:3", "4:3"),
        ("16:9", "16:9"),
        ("16:10", "16:10"),
    ]

    screen_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    orientation = models.CharField(
        max_length=10,
        choices=ORIENTATION_CHOICES,
        default="landscape",
        blank=True,
        null=True,
    )
    ratio = models.CharField(
        max_length=10, choices=RATIO_CHOICES, default="16:9", blank=True, null=True
    )
    size = models.PositiveIntegerField(
        help_text="diagonal en pulgadas", blank=True, null=True
    )
    has_audio = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class StopScreen(Screen):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    def __str__(self):
        return self.stop.stop_name


class StationScreen(Screen):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    point = models.PointField(blank=True, null=True)
    stops = models.ManyToManyField(Stop, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.station.station_name


class VehicleScreen(Screen):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.vehicle.vehicle_label
