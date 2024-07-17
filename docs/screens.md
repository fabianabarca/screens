# Despliegue de datos en pantallas

Hay tres tipos de pantallas:

- En paradas
- En estaciones, con varias paradas
- En vehículos

## Pantallas en paradas

Sirve a una única parada y sus rutas.

### Información estática

Carga al inicio de la operación de la pantalla desde `views.py`.

- **Nombre de la parada o estación**: desde 
- **Hora actual**: provista por el navegador cliente
- **Otra información**:
  - Tasa de actualización

### Información en tiempo real

Actualizada cada $T$ segundos desde `tasks.py` con Celery y enviados al navegador de la pantalla con WebSockets.

Lista de viajes que pasarán por la parada (`array`, mostrar primeros N). Averiguamos los viajes que van a pasar por la parada. 

```bash
trips = GET https://datahub.bucr.digital/api/trip-updates?stop_id=23549 
```

`for trip in trips:` 

- **Código de la ruta** (L1, L2) `trip_route_id`: y de ahí buscar `route_short_name` con 
```bash
GET https://datahub.bucr.digital/api/routes?route_id=trip.trip_route_id
```
- **Nombre de la ruta** `route_long_name` (sale igual que arriba)
- **Destino de la ruta** (Educación, Artes Plásticas...) 
```bash
GET https://datahub.bucr.digital/api/trips?trip_id=trip_trip_id 
```
y de ahí sacar `trip_headsign`.
- **Nivel de ocupación** (primeros K, posiblemente solo uno): `EMPTY`, MANY_SEATS_AVAILABLE, FEW_SEATS_AVAILABLE, STANDING_ROOM_ONLY, CRUSHED_STANDING_ROOM_ONLY, FULL, NOT_ACCEPTING_PASSENGERS, NO_DATA_AVAILABLE, NOT_BOARDABLE: desde vehicle_occupancy_status
```bash
GET https://datahub.bucr.digital/api/vehicle-positions?vehicle_trip_trip_id=trip_trip_id
```
- **Otra información** (accesibilidad, etc.): `vehicle_vehicle_wheelchair_accessible`
- **Tiempo estimado de llegada** (en minutos) `arrival_time`: calcular desde arrival_time (hacer el cálculo de la diferencia de tiempo)
```bash
GET https://datahub.bucr.digital/api/stop-time-update?trip_update=trip_trip_id&stop_id=23549
```

### Estructura del mensaje vía WebSockets

Para una solicitud al *endpoint* `/next-trips` a las 15:16:00, entonces:

```json
{
    [
        {
            "stop_id": "KJDH23",
            "next_trips": [
                {
                    "trip_id": "L1-33",
                    "route_short_name": "L1",
                    "route_long_name": "Bus UCR (L1) con milla",
                    "trip_headsign": "Educación",
                    "wheelchair_accessible": "WHEELCHAIR_ACCESSIBLE",
                    "arrival_time": "15:17:00",
                    "in_progress": true,
                    "journey": {
                        "position_in_shape": 0.465,
                        "current_stop_sequence": 23,
                        "current_status": "INCOMING_AT",
                        "occupancy_status": "CRUSHED_STANDING_ROOM_ONLY"
                    }
                },
                {
                    "trip_id": "L2-12",
                    "route_short_name": "L2",
                    "route_long_name": "Bus UCR (L2) sin milla",
                    "trip_headsign": "Artes Plásticas",
                    "wheelchair_accessible": "WHEELCHAIR_ACCESSIBLE",
                    "arrival_time": "15:23:00",
                    "in_progress": true,
                    "journey": {
                        "position_in_shape": 0.391,
                        "current_stop_sequence": 14,
                        "current_status": "STOPPED_AT",
                        "occupancy_status": "FEW_SEATS_AVAILABLE"
                    }
                },
                {
                    "trip_id": "L1-34",
                    "route_short_name": "L1",
                    "route_long_name": "Bus UCR (L2) sin milla",
                    "trip_headsign": "Educación",
                    "wheelchair_accessible": "WHEELCHAIR_ACCESSIBLE",
                    "arrival_time": "15:34:00",
                    "in_progress": false
                }
            ]
        },
        {
            "stop_id": "JHE054",
            "next_trips": [
                {
                    "trip_id": "L1-33",
                    "route_short_name": "L1",
                    "route_long_name": "Bus UCR (L1) con milla",
                    "trip_headsign": "Educación",
                    "wheelchair_accessible": "WHEELCHAIR_ACCESSIBLE",
                    "arrival_time": "15:17:00",
                    "in_progress": true,
                    "journey": {
                        "position_in_shape": 0.465,
                        "current_stop_sequence": 23,
                        "current_status": "INCOMING_AT",
                        "occupancy_status": "CRUSHED_STANDING_ROOM_ONLY"
                    }
                }
            ]
        }
    ]
}


```

Notas:

- Los minutos faltantes para la llegada de cada viaje son estimados con `arrival_time` y la hora actual.
- "0 minutos" significa que el bus está en la parada o llegará dentro del margen de precisión de la estimación.
- El `array` enviado debe estar ordenado según orden creciente de `arrival_time`.
- Asunto de próximas llegadas para viajes en progreso versus viajes programados (`stop_times`). Nota: resuelto con `in_progress` y será evaluado del lado del servidor concentrador de datos en el API.