from django.contrib.gis import admin
from .models import InfoProvider, Screen, Stop

# Register your models here.

admin.site.register(InfoProvider)
admin.site.register(Screen, admin.GISModelAdmin)
admin.site.register(Stop, admin.GISModelAdmin)
