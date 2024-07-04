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
    """Retrieves new real-time information and updates the connected screens.
    """
    
    with open("test.json", "r") as file:
        update_message = file.read()
    
    update_message = json.loads(update_message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "screen",
        {
            "type": "screen_message",
            "message": update_message,
        },
    )
    
    return "Actualización de pantallas exitosa"


@shared_task
def get_gtfs():
    return "GTFS"