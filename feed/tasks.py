# Create your tasks here

from feed.models import InfoProvider, StopScreen, Stop, Station, StationScreen

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import requests
from datetime import datetime


@shared_task
def update_stop_screens():
    """Retrieves new real-time information and updates the connected screens fro a given stop."""

    info_provider = InfoProvider.objects.get(is_active=True)
    stop_screens = StopScreen.objects.filter(is_active=True)

    for screen in stop_screens:

        stop = screen.stop

        api_url = info_provider.api_url
        endpoint = "next-trips"
        url = api_url + endpoint
        params = {"stop_id": stop.stop_id}
        response = requests.get(url, params=params)

        if response.status_code == 200:

            stop_message = response.json()
            update_message = stop_message

            # Send the message to the screen via websocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"screen_stop_{screen.screen_id}",
                {
                    "type": "screen_message",
                    "message": update_message,
                },
            )

        else:

            print(f"Error: {response.status_code}")

    # Status monitor update
    message = {}
    message["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message["active_stop_screens"] = len(stop_screens)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "status",
        {
            "type": "status_message",
            "message": message,
        },
    )

    return "Actualización de pantallas exitosa"


@shared_task
def update_station_screens():
    """Retrieves new real-time information and updates the connected screens for a given station that comprises two or more stops."""

    info_provider = InfoProvider.objects.get(is_active=True)
    station_screens = StationScreen.objects.filter(is_active=True)

    for screen in station_screens:

        stops = Stop.objects.filter(parent_station=screen.station)
        update_message = []

        for stop in stops:

            api_url = info_provider.api_url
            endpoint = "next-trips"
            url = api_url + endpoint
            params = {"stop_id": stop.stop_id}
            response = requests.get(url, params=params)

            if response.status_code == 200:

                stop_message = response.json()
                update_message.append(stop_message)
            
            else:

                print(f"Error: {response.status_code}")

        # Send the message to the screen via websocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"screen_station_{screen.screen_id}",
            {
                "type": "screen_message",
                "message": update_message,
            },
        )


    # Status monitor update via WebSockets. TODO: Prometheus
    message = {}
    message["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message["active_stop_screens"] = len(station_screens)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "status",
        {
            "type": "status_message",
            "message": message,
        },
    )

    return "Actualización de pantallas exitosa"


@shared_task
def update_stops():
    """Retrieves and updates stops."""

    info_provider = InfoProvider.objects.get(is_active=True)
    try:
        response = requests.get(info_provider.api_url + "stops")
        response.raise_for_status()
        stops = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stops: {e}")
        return "Error fetching stops"
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return "Error parsing JSON response"

    # Save stations
    for stop in stops:
        location_type = stop["location_type"]
        if location_type == 1:
            stop_id = stop["stop_id"]
            stop_code = stop["stop_code"]
            stop_name = stop["stop_name"]
            stop_desc = stop["stop_desc"]
            stop_point = stop["stop_point"]
            wheelchair_boarding = stop["wheelchair_boarding"]
            Station.objects.update_or_create(
                stop_id=stop_id,
                defaults={
                    "stop_code": stop_code,
                    "stop_name": stop_name,
                    "stop_desc": stop_desc,
                    "stop_point": stop_point,
                    "location_type": location_type,
                    "wheelchair_boarding": wheelchair_boarding,
                },
            )

    # Save stops
    for stop in stops:
        location_type = stop["location_type"]
        if location_type == 0:
            stop_id = stop["stop_id"]
            stop_code = stop["stop_code"]
            stop_name = stop["stop_name"]
            stop_desc = stop["stop_desc"]
            stop_point = stop["stop_point"]
            stop_heading = stop["stop_heading"]
            wheelchair_boarding = stop["wheelchair_boarding"]
            parent_station = stop["parent_station"]
            if parent_station:
                parent_station = Station.objects.get(stop_id=parent_station)
            else:
                parent_station = None
            Stop.objects.update_or_create(
                stop_id=stop_id,
                defaults={
                    "stop_code": stop_code,
                    "stop_name": stop_name,
                    "stop_desc": stop_desc,
                    "stop_point": stop_point,
                    "location_type": location_type,
                    "stop_heading": stop_heading,
                    "wheelchair_boarding": wheelchair_boarding,
                    "parent_station": parent_station,
                },
            )

    return "Actualización de paradas exitosa"
