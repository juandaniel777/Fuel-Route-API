import pandas as pd
import requests
import time
import re

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

INPUT_FILE = "fuel-prices-cleaned.csv"
OUTPUT_FILE = "fuel_with_coordinates.csv"
USER_AGENT = "fuel-route-assessment-app"

# ---------------------------------------------------
# SESSION + CACHE
# ---------------------------------------------------

session = requests.Session()
cache = {}


# ---------------------------------------------------
# NORMALIZE INTERSECTION TEXT
# ---------------------------------------------------

def normalize_intersection(address):
    """
    Cleans intersection text like:
    "I-85,  EXIT 22 & CR-138"
    -> "I-85 & CR-138"
    """

    if pd.isna(address):
        return ""

    address = address.upper()

    # Remove EXIT references
    address = re.sub(r"EXIT\s*\d+", "", address)

    # Remove extra commas
    address = address.replace(",", "")

    # Normalize spacing
    address = re.sub(r"\s+", " ", address)

    return address.strip()


# ---------------------------------------------------
# GEOCODING FUNCTION (STRUCTURED + FALLBACK)
# ---------------------------------------------------

def geocode_address(street, city, state):
    cache_key = f"{street}-{city}-{state}"

    if cache_key in cache:
        return cache[cache_key]

    url = "https://nominatim.openstreetmap.org/search"

    headers = {
        "User-Agent": USER_AGENT
    }

    # 1️⃣ Try structured street search
    params = {
        "street": street,
        "city": city,
        "state": state,
        "country": "USA",
        "format": "json",
        "limit": 1
    }

    response = session.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    # 2️⃣ Fallback → city center
    if not data:
        print(f"⚠ Intersection failed, fallback to city for {city}")

        params = {
            "city": city,
            "state": state,
            "country": "USA",
            "format": "json",
            "limit": 1
        }

        response = session.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            cache[cache_key] = (None, None)
            return None, None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    cache[cache_key] = (lat, lon)
    return lat, lon


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():
    df = pd.read_csv(INPUT_FILE)

    latitudes = []
    longitudes = []

    total = len(df)

    for index, row in df.iterrows():
        cleaned_street = normalize_intersection(row["Address"])

        lat, lon = geocode_address(
            cleaned_street,
            row["City"],
            row["State"]
        )

        print(f"[{index+1}/{total}] {row['Truckstop Name']} → {lat}, {lon}")

        latitudes.append(lat)
        longitudes.append(lon)

        # Respect Nominatim rate limit (1 req/sec)
        
        #time.sleep(1)

    df["latitude"] = latitudes
    df["longitude"] = longitudes

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nGeocoding completed and saved to:", OUTPUT_FILE)


# ---------------------------------------------------

if __name__ == "__main__":
    main()
