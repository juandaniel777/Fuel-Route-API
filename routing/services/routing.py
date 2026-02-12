# routing/services/routing.py
import polyline
import requests
from django.conf import settings
from config.settings import ORS_API_KEY
import folium

ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

def get_route(start, end):

    headers = {"Authorization": ORS_API_KEY, 
               "Content-Type": "application/json; charset=utf-8",
               "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
               }
    body = {
        "coordinates": [start, end],
        "instructions": False
    }

    response = requests.post(ORS_URL, json=body, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
   # print("ORS response:", data)  # Debug print

    route = data["routes"][0]
    encoded = route["geometry"]
    decoded_coords = polyline.decode(encoded)
   # print("Decoded coordinates:", decoded_coords)  # Debug print


    # Create map centered on first point
    #m = folium.Map(location=decoded_coords[0], zoom_start=13)

# Add polyline (folium expects lat, lon)
    #folium.PolyLine(decoded_coords).add_to(m)

    #m.save("route_map.html")
    return {
     "geometry": decoded_coords,
        "distance_m": route["summary"]["distance"],  # meters
        "duration_s": route["summary"]["duration"]
    }

def plot_route_with_fuel(decoded_coords, fuel_stops, map_file="route_map.html"):
    """
    Plot route and fuel stops on folium map
    """
    m = folium.Map(location=decoded_coords[0], zoom_start=6)
    folium.PolyLine(decoded_coords, color="blue", weight=5, opacity=0.7).add_to(m)

    for name, address, lat, lon, price, refill_cost in fuel_stops:
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b><br>{address}<br>Price: ${price:.2f}/gallon<br>Refill cost: ${refill_cost:.2f}",
            icon=folium.Icon(color="green", icon="fa-gas-pump", prefix='fa')
        ).add_to(m)

    m.save(map_file)
    return map_file