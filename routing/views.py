from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from rest_framework.views import APIView,View
from rest_framework.response import Response
from routing.services.routing import get_route , plot_route_with_fuel
from routing.services.fuel_optimizer import optimize_fuel , MAX_RANGE, MPG
import pandas as pd
import os
from django.conf import settings
# Load fuel stops CSV once (best practice)
df_fuel = pd.read_csv("fuel_with_coordinates.csv")
fuel_stops_list = list(zip(
    df_fuel["Truckstop Name"],
    df_fuel["Address"],
    df_fuel["latitude"],
    df_fuel["longitude"],
    df_fuel["Retail Price"]
))

class RouteAPIView(APIView):
    def post(self, request):
        start = request.data["start"]  # [lng, lat]
        end = request.data["end"]

        route = get_route(start, end)
        decoded_coords = route["geometry"]
       # print("Decoded coordinates:", fuel_stops_list)
         # Get optimized fuel stops
        fuel_stops_selected = optimize_fuel(decoded_coords, fuel_stops_list)

        # Plot route and fuel stops
        map_file = plot_route_with_fuel(decoded_coords, fuel_stops_selected)

        # Calculate totals
        distance_miles = route["distance_m"] * 0.000621371
        fuel_used_gallons = distance_miles / MPG
        total_cost = sum(stop[5] for stop in fuel_stops_selected)  # refill cost

        # Prepare fuel stop data
        stops_data = [
            {
                "name": stop[0],
                "address": stop[1],
                "lat": stop[2],
                "lng": stop[3],
                "price_per_gallon": stop[4],
                "refill_cost": stop[5]
            }
            for stop in fuel_stops_selected
        ]
 # Absolute URL to /map/ endpoint
        map_url = request.build_absolute_uri(reverse("map-view"))

        return Response({
            "distance_miles": round(distance_miles, 2),
            "fuel_used_gallons": round(fuel_used_gallons, 2),
            "total_fuel_cost": round(total_cost, 2),
            "fuel_stops": stops_data,
           # "route": decoded_coords,
            "map_file": map_file,
            "map_url": map_url
        })
class MapView(View):
    def get(self, request, *args, **kwargs):
        # Path to the generated map HTML file
        map_file_path = os.path.join(settings.BASE_DIR, "route_map.html")
        
        if not os.path.exists(map_file_path):
            return HttpResponse("Map file not found. Generate a route first.", status=404)
        
        # Return the HTML file directly
        return FileResponse(open(map_file_path, "rb"), content_type="text/html")