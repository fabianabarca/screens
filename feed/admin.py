from django.contrib.gis import admin
from .models import InfoProvider, Stop, Station, Vehicle, StopScreen, StationScreen, VehicleScreen

# Register your models here.

admin.site.register(InfoProvider)
admin.site.register(Stop, admin.GISModelAdmin)
admin.site.register(Station, admin.GISModelAdmin)
admin.site.register(Vehicle)
admin.site.register(StopScreen, admin.GISModelAdmin)
admin.site.register(StationScreen, admin.GISModelAdmin)
admin.site.register(VehicleScreen)
