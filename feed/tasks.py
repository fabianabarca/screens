# Create your tasks here

from feed.models import InfoProvider, Screen

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import requests
from time import sleep
import json


@shared_task
def update_screens():
    """Retrieves new real-time information and updates the connected screens."""

    info_provider = InfoProvider.objects.get(is_active=True)
    screens = Screen.objects.filter(is_active=True)

    for screen in screens:

        stops = screen.stops.all()

        for stop in stops:

            url = info_provider.api_url
            params = {"stop_id": stop.stop_id}
            response = requests.get(url, params=params)

            if response.status_code == 200:

                stop_message = response.json()
                
                # --- Simulate a request to the API ---
                #with open("test.json", "r") as file:
                #    update_message = file.read()
                #update_message = json.loads(update_message)
                # --------------------------------------

                update_message = stop_message["next_arrivals"]

                # Send the message to the screen via websocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"screen_{screen.screen_id}",
                    {
                        "type": "screen_message",
                        "message": update_message,
                    },
                )

            else:
                
                print(f"Error: {response.status_code}")

    return "Actualización de pantallas exitosa"


@shared_task
def get_gtfs():
    return "GTFS"


@shared_task
def update_stops():
    return "Stops are updated"
