# Create your tasks here

from feed.models import Screen

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import requests
from time import sleep
import json


@shared_task
def update_screens():
    """Retrieves new real-time information and updates the connected screens."""

    screens = Screen.objects.filter(is_active=True)

    for screen in screens:

        stops = screen.stops.all()
        # update_message = []

        for stop in stops:

            url = f"https://datahub.bucr.digital/api/next-trips?stop_id={stop.stop_id}"
            # response = requests.get(url)
            # TODO: Give new format to update_message
            # stop_message = {}
            # stop_message["stop_id"] = stop.stop_id
            # stop_message["next_trips"] = response.json()
            # update_message.append(stop_message)

            # --- Simulate a request to the API ---
            with open("test.json", "r") as file:
                update_message = file.read()
            update_message = json.loads(update_message)
            # --------------------------------------

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"screen_{screen.screen_id}",
                {
                    "type": "screen_message",
                    "message": update_message,
                },
            )

    return "Actualización de pantallas exitosa"


@shared_task
def get_gtfs():
    return "GTFS"


@shared_task
def update_stops():
    return "Stops are updated"
