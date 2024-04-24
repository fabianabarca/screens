from django.contrib.gis import admin
from .models import Screen

# Register your models here.

admin.site.register(Screen, admin.GISModelAdmin)
