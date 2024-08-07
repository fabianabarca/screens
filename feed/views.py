from django.shortcuts import render
from .models import Screen
import random

# Create your views here.


def screens(request):
    return render(request, "screens.html")


def create_screen(request):
    return render(request, "create_screen.html")


def screen(request, screen_id):
    screen = Screen.objects.get(screen_id=screen_id)
    if screen.location == "stop":
        context = {"screen": screen}
        return render(request, "test_screen.html", context)


def edit_screen(request, screen_id):
    context = {"screen_id": screen_id}
    return render(request, "edit_screen.html", context)


def update_screen(request, screen_id):
    # Get a Django Signal signaling that the FeedMessage has been processed and there are updates for each stop.
    # For each screen, collect all data linked to it and send it, with a given format, to the screen via websocket.
    return 0
