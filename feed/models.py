from django.contrib.gis.db import models

# Create your models here.


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
    stop_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Latitud de la parada.",
    )
    stop_lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Longitud de la parada.",
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
    stop_timezone = models.CharField(
        max_length=255, blank=True, help_text="Zona horaria de la parada."
    )
    wheelchair_boarding = models.PositiveIntegerField(
        blank=True, null=True, help_text="Acceso para sillas de ruedas."
    )
    level_id = models.CharField(
        max_length=255, blank=True, help_text="Identificador del nivel."
    )
    platform_code = models.CharField(
        max_length=255, blank=True, help_text="Código de la plataforma."
    )

    def __str__(self):
        return self.stop_name


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
    LOCATION_CHOICES = [
        ("stop", "Parada única"),
        ("station", "Estación con varias paradas"),
        ("vehicle", "Pantalla en el vehículo"),
    ]

    screen_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(
        max_length=10, choices=LOCATION_CHOICES, blank=True, null=True
    )
    point = models.PointField(blank=True, null=True)
    stops = models.ManyToManyField(Stop, blank=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
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

    def __str__(self):
        return self.name
