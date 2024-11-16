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

    # def save(self, *args, **kwargs):
    #    if self.is_active:
    #        InfoProvider.objects.filter(is_active=True).update(is_active=False)
    #    super(InfoProvider, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class StopBase(models.Model):
    """Individual locations where vehicles pick up or drop off riders.
    Maps to stops.txt in the GTFS feed.

    TODO: check wheelchair_boarding choices (different for stops and stations)
    """

    WHEELCHAIR_BOARDING_CHOICES = [
        (0, "Sin información"),
        (1, "Accesible"),
        (2, "No accesible"),
    ]

    stop_id = models.CharField(
        max_length=255, primary_key=True, help_text="Identificador único de la parada."
    )
    stop_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Código de la parada, visible en el URL.",
    )
    stop_name = models.CharField(max_length=255, help_text="Nombre de la parada.")
    stop_desc = models.TextField(
        blank=True, null=True, help_text="Descripción de la parada."
    )
    stop_point = models.PointField(
        blank=True, null=True, help_text="Punto georreferenciado de la parada."
    )
    location_type = models.PositiveIntegerField(blank=True, null=True)
    wheelchair_boarding = models.PositiveIntegerField(
        blank=True, null=True, choices=WHEELCHAIR_BOARDING_CHOICES
    )

    class Meta:
        abstract = True


class Station(StopBase):
    """A group of related stops where vehicles pick up or drop off riders.
    Maps to stops.txt in the GTFS feed.
    """

    def __str__(self):
        return self.stop_name


class Stop(StopBase):

    STOP_HEADING_CHOICES = [
        ("north", "norte"),
        ("northeast", "noreste"),
        ("east", "este"),
        ("southeast", "sureste"),
        ("south", "sur"),
        ("southwest", "suroeste"),
        ("west", "oeste"),
        ("northwest", "noroeste"),
    ]
    stop_heading = models.CharField(
        max_length=10,
        choices=STOP_HEADING_CHOICES,
        blank=True,
        null=True,
    )
    parent_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        if self.stop_heading:
            return f"{self.stop_id}: {self.stop_name} ({self.stop_heading})"
        return f"{self.stop_id}: {self.stop_name}"


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

    screen_id = models.AutoField(primary_key=True)
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


class StopScreen(Screen):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_slug = models.SlugField(unique=True)
    # TODO: fields for heading and for screen layout

    def __str__(self):
        return f"{self.stop.stop_name} ({self.screen_id})"


class StationScreen(Screen):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    station_slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.station.station_name} ({self.screen_id})"


class VehicleScreen(Screen):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vehicle_slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.vehicle.vehicle_label} ({self.screen_id})"
