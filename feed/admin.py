from django.contrib.gis import admin
from .models import Screen, Stop

# Register your models here.

admin.site.register(Screen, admin.GISModelAdmin)
admin.site.register(Stop, admin.GISModelAdmin)
