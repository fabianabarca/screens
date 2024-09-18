from django.shortcuts import render
from feed.models import Stop, Station, Vehicle, StopScreen, StationScreen, VehicleScreen
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "index.html")


def stop(request):
    return render(request, "stop.html")


def stop_screen_create(request):
    return render(request, "stop_screen_create.html")


def stop_screen(request, stop_slug):
    stop = Stop.objects.get(stop_slug=stop_slug)
    screen = StopScreen.objects.get(stop=stop)
    context = {"screen": screen, "stop": stop}
    return render(request, "test_screen.html", context)


def stop_screen_edit(request, stop_slug):
    context = {"stop_slug": stop_slug}
    return render(request, "stop_screen_edit.html", context)


def station(request):
    return render(request, "station.html")


def station_screen_create(request):
    return render(request, "station_screen_create.html")


def station_screen(request, station_slug):
    station = Station.objects.get(station_slug=station_slug)
    screen = StationScreen.objects.get(station=station)
    context = {"screen": screen, "station": station}
    return render(request, "station_screen.html", context)


def station_screen_edit(request, station_slug):
    context = {"screen_id": station_slug}
    return render(request, "station_screen_edit.html", context)


def vehicle(request):
    return render(request, "vehicle.html")


def vehicle_screen_create(request):
    return render(request, "vehicle_screen_create.html")


def vehicle_screen(request, vehicle_slug):
    screen = VehicleScreen.objects.get(screen_id=vehicle_slug)
    context = {"screen": screen}
    return render(request, "vehicle_screen.html", context)


def vehicle_screen_edit(request, vehicle_slug):
    context = {"screen_id": vehicle_slug}
    return render(request, "vehicle_screen_edit.html", context)


def update_screen(request, screen_id):
    # Get a Django Signal signaling that the FeedMessage has been processed and there are updates for each stop.
    # For each screen, collect all data linked to it and send it, with a given format, to the screen via websocket.
    return 0


def about(request):
    return render(request, "about.html")


def profile(request):
    return render(request, "profile.html")
