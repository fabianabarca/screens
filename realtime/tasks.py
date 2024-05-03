from celery import shared_task
import requests


@shared_task
def get_updates():
    # Logic to get updates from the server and process them
    return # JSON that goes to the screen with data to be displayed

"""
{
    "data": [
        {
            "route_id": 1,
            "route_name": "John Doe",
            "trip_eta": 25,
            "occupancy_status": "FULL"
        },
        {
            "route_id": 2,
            "route_name": "Jane Doe",
            "trip_eta": 24,
            "occupancy_status": "MANY_SEATS_AVAILABLE"
        }
    ]
}
"""