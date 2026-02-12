# routing/services/fuel_optimizer.py
import polyline
from geopy.distance import geodesic
from routing.models import FuelStation
import math
# routing/services/fuel_optimizer.py
from geopy.distance import geodesic

MAX_RANGE = 500       # Maximum miles per tank
BUFFER = 450          # Start looking for fuel when this much miles remain
MPG = 10              # Miles per gallon

def optimize_fuel(route_coords, fuel_stops):
    """
    route_coords: list of (lat, lon)
    fuel_stops: list of tuples (name, address, lat, lon, price)
    
    Returns list of fuel stops along the route with refill cost
    """
    selected_stops = []
    distance_acc = 0
    last_point = route_coords[0]

    for point in route_coords[1:]:
        segment_distance = geodesic(last_point, point).miles
        distance_acc += segment_distance

        if distance_acc >= BUFFER:
            # Find cheapest station nearby within 50 miles
            station = find_cheapest_station(point, fuel_stops, radius=50)
            if station and station not in selected_stops:
                name, address, lat, lon, price = station
                refill_cost = (MAX_RANGE / MPG) * price
                selected_stops.append((name, address, lat, lon, price, refill_cost))
                distance_acc = 0  # reset tank
        last_point = point

    return selected_stops

def find_cheapest_station(point, fuel_stops, radius=50):
    """
    point: (lat, lon)
    fuel_stops: list of tuples (name, address, lat, lon, price)
    radius: miles
    """

    # Filter out stops with invalid coordinates (None or NaN)
    valid_stops = [
        s for s in fuel_stops
        if s[2] is not None and s[3] is not None and 
           not math.isnan(s[2]) and not math.isnan(s[3])
    ]

    if not valid_stops:
        return None

    # Filter by distance
    nearby = [
        s for s in valid_stops
        if geodesic(point, (s[2], s[3])).miles <= radius
    ]

    if not nearby:
        return None

    # Return the cheapest fuel stop
    return min(nearby, key=lambda s: s[4])