import pandas as pd
from Geocoding import geocode_address, geocode_with_intersection
import time

df = pd.read_csv("fuel-prices-for-be-assessment.csv")

latitudes = []
longitudes = []

for index, row in df.iterrows():
    #full_address = f"{row['Address']}, {row['City']}, {row['State']}, USA"

    #lat, lon = geocode_address(full_address)
    lat, lon = geocode_with_intersection(row)


    latitudes.append(lat)
    longitudes.append(lon)

    print(f"Geocoded: {row['Truckstop Name']} -> {lat}, {lon}")

    #time.sleep(1)  # VERY IMPORTANT (rate limit)

df["latitude"] = latitudes
df["longitude"] = longitudes

df.to_csv("fuel_with_coordinates.csv", index=False)
