from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("parada/", views.stop, name="stop"),
    path("parada/crear/", views.stop_screen_create, name="stop_screen_create"),
    path("parada/<str:screen_id>/", views.stop_screen, name="stop_screen"),
    path("parada/<str:screen_id>/editar/", views.stop_screen_edit, name="stop_screen_edit"),
    path("estacion/", views.station, name="station"),
    path("estacion/crear/", views.station_screen_create, name="station_screen_create"),
    path("estacion/<str:screen_id>/", views.station_screen, name="station_screen"),
    path("estacion/<str:screen_id>/editar/", views.station_screen_edit, name="station_screen_edit"),
    path("vehiculo/", views.vehicle, name="vehicle"),
    path("vehiculo/crear/", views.vehicle_screen_create, name="vehicle_screen_create"),
    path("vehiculo/<str:screen_id>/", views.vehicle_screen, name="vehicle_screen"),
    path("vehiculo/<str:screen_id>/editar/", views.vehicle_screen_edit, name="vehicle_screen_edit"),
    path("sobre/", views.about, name="about"),
    path("perfil/", views.profile, name="profile"),
]
