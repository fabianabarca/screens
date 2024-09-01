from django.shortcuts import render
from feed.models import StopScreen, StationScreen, VehicleScreen

# Create your views here.


def index(request):
    return render(request, "index.html")


def stop(request):
    return render(request, "stop.html")


def stop_screen_create(request):
    return render(request, "stop_screen_create.html")


def stop_screen(request, screen_id):
    screen = StopScreen.objects.get(screen_id=screen_id)
    context = {"screen": screen}
    return render(request, "test_screen.html", context)


def stop_screen_edit(request, screen_id):
    context = {"screen_id": screen_id}
    return render(request, "stop_screen_edit.html", context)


def station(request):
    return render(request, "station.html")


def station_screen_create(request):
    return render(request, "station_screen_create.html")


def station_screen(request, screen_id):
    screen = StationScreen.objects.get(screen_id=screen_id)
    context = {"screen": screen}
    return render(request, "station_screen.html", context)


def station_screen_edit(request, screen_id):
    context = {"screen_id": screen_id}
    return render(request, "station_screen_edit.html", context)


def vehicle(request):
    return render(request, "vehicle.html")


def vehicle_screen_create(request):
    return render(request, "vehicle_screen_create.html")


def vehicle_screen(request, screen_id):
    screen = VehicleScreen.objects.get(screen_id=screen_id)
    context = {"screen": screen}
    return render(request, "vehicle_screen.html", context)


def vehicle_screen_edit(request, screen_id):
    context = {"screen_id": screen_id}
    return render(request, "vehicle_screen_edit.html", context)


def update_screen(request, screen_id):
    # Get a Django Signal signaling that the FeedMessage has been processed and there are updates for each stop.
    # For each screen, collect all data linked to it and send it, with a given format, to the screen via websocket.
    return 0


def about(request):
    return render(request, "about.html")


def profile(request):
    return render(request, "profile.html")
