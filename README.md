# Fuel Route API

A Django REST API that optimizes fuel stops along vehicle routes by calculating the most cost-effective refueling strategy based on real-time fuel prices and road distances.

## 🎯 Overview

This project combines route optimization with fuel price analysis to help drivers find the most economical way to refuel during long trips. It uses OpenRouteService for route planning and integrates fuel station data with pricing information to recommend optimal refueling stops.

## ✨ Features

- **Route Optimization**: Calculate the most efficient driving route between two locations using OpenRouteService API
- **Fuel Stop Optimization**: Intelligently identify fuel stops along the route based on vehicle range and fuel prices
- **Cost Analysis**: Calculate refueling costs for each recommended fuel stop
- **Interactive Route Visualization**: Generate interactive maps with route and fuel stop locations using Folium
- **Data Cleaning**: Tools to clean and prepare fuel pricing data
- **Geocoding Support**: Add geographic coordinates to fuel station data

## 🛠 Tech Stack

- **Framework**: Django 6.0.2 + Django REST Framework
- **Language**: Python 3.x
- **APIs**: OpenRouteService (routing)
- **Database**: SQLite
- **Libraries**:
  - `folium` - Interactive map generation
  - `geopy` - Geographic distance calculations
  - `polyline` - Route encoding/decoding
  - `requests` - HTTP requests
  - `python-dotenv` - Environment variable management

## 📋 Project Structure

```
fuel_route_api/
├── config/                          # Django configuration
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # URL routing
│   └── wsgi.py                     # WSGI application
├── routing/                         # Main routing app
│   ├── models.py                   # Database models
│   ├── views.py                    # API endpoints
│   ├── serializers.py              # DRF serializers
│   └── services/
│       ├── routing.py              # Route calculation logic
│       └── fuel_optimizer.py       # Fuel stop optimization
├── manage.py                        # Django management script
├── cleaner.py                      # Data cleaning utilities
├── AddCoordinates.py               # Geocoding utility
├── Geocoding.py                    # Additional geocoding functions
├── route_map.html                  # Generated route visualization
├── db.sqlite3                      # SQLite database
├── .env                            # Environment variables
└── requirements.txt                # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenRouteService API key (get one at https://openrouteservice.org/)

### Installation

1. **Clone/Navigate to the project**
   ```bash
   cd fuel_route_api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   ORS_API_KEY=your_openrouteservice_api_key_here
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 📡 API Usage

### Get Optimized Route with Fuel Stops

**Endpoint**: `POST /api/route/optimize/`

**Request body**:
```json
{
  "start": [lon, lat],
  "end": [lon, lat]
}
```

**Response**:
```json
{
  "route": {
    "geometry": [[lat, lon], ...],
    "distance_m": 500000,
    "duration_s": 18000
  },
  "fuel_stops": [
    {
      "name": "Station Name",
      "address": "Address",
      "lat": 40.7128,
      "lon": -74.0060,
      "price": 3.50,
      "refill_cost": 175.00
    }
  ],
  "map_file": "route_map.html",
  "map_url": "http://127.0.0.1:8000/map/"
}
```

## ⚙️ Configuration

### Fuel Optimizer Settings

In `routing/services/fuel_optimizer.py`, adjust these constants:

```python
MAX_RANGE = 500        # Maximum miles per tank
BUFFER = 450           # Start looking for fuel when this distance remains
MPG = 10               # Vehicle miles per gallon
```

### Search Radius

Fuel stops are searched within a **50-mile radius** of the current route position. Modify in `fuel_optimizer.py`:

```python
station = find_cheapest_station(point, fuel_stops, radius=50)
```

## 🧹 Data Processing

### Clean Fuel Price Data

Use the `cleaner.py` script to process raw fuel pricing data:

```bash
python cleaner.py
```

### Add Coordinates to Fuel Stations

Geocode fuel station addresses:

```bash
python AddCoordinates.py
```

## 🗺️ Route Visualization

The API automatically generates an interactive HTML map (`route_map.html`) showing:
- Route path (blue line)
- Recommended fuel stops (green markers with gas pump icons)
- Fuel prices and refill costs in popup

Open `route_map.html` in a web browser to view the map.

## 📦 Required Files

Ensure these CSV files are present for fuel data:

- `fuel-prices-for-be-assessment.csv` - Raw fuel price data
- `fuel_with_coordinates.csv` - Processed fuel data with coordinates

## 🔐 Security Notes

- ⚠️ **WARNING**: `SECRET_KEY` in `settings.py` is exposed. Change it before production.
- ⚠️ **WARNING**: `DEBUG = True` is enabled. Set to `False` in production.
- Store `ORS_API_KEY` securely in environment variables (`.env` file).
- Never commit `.env` to version control.

## 🚧 Development

### Running Tests

```bash
python manage.py test
```

### Database Shell

```bash
python manage.py shell
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 Data Flow

1. **Input**: Start and end coordinates
2. **Route Calculation**: OpenRouteService calculates optimal driving route
3. **Route Decoding**: Polyline-encoded route is decoded into coordinate points
4. **Fuel Optimization**: Algorithm identifies optimal refueling stops based on:
   - Vehicle range (500 miles max)
   - Current fuel consumption
   - Available fuel stations within 50-mile radius
   - Fuel prices at each station
5. **Output**: Route geometry, fuel stops with costs, and interactive map

## 🤝 Contributing

Feel free to submit issues and enhancement requests.

## 📄 License

This project is provided as-is for development and assessment purposes.

## 📧 Support

For questions or issues, please check the project documentation or contact the development team.
