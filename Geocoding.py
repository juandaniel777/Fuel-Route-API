import requests
import time
import re


def normalize_intersection(address: str) -> str:
    """
    Convert:
    'I-44, EXIT 283 & US-69'
    into:
    'I-44 & US-69'
    """

    # Remove EXIT numbers
    address = re.sub(r"EXIT\s*\d+", "", address, flags=re.IGNORECASE)

    # Remove extra commas
    address = address.replace(",", " ")

    # Remove extra spaces
    address = re.sub(r"\s+", " ", address).strip()

    return address





def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "fuel-route-app"  # REQUIRED by Nominatim
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()

    if not data:
        return None, None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    return lat, lon



def geocode_with_intersection(row):
    """
    Full robust geocoding:
    1) Try cleaned intersection
    2) Fallback to city/state
    """

    cleaned = normalize_intersection(row["Address"])

    full_query = f"{cleaned}, {row['City']}, {row['State']}, USA"

    lat, lon = geocode_address(full_query)

    if lat is None:
        print(f"Intersection failed, fallback to city for {row['City']}")
        fallback_query = f"{row['City']}, {row['State']}, USA"
        lat, lon = geocode_address(fallback_query)

    return lat, lon