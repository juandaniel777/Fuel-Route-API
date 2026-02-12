# routing/management/commands/load_fuel_data.py
import csv
from django.core.management.base import BaseCommand
from routing.models import FuelStation

class Command(BaseCommand):

    help = "Load fuel station data from CSV"
    def handle(self, *args, **kwargs):
        with open("fuel-prices-for-be-assessment.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                FuelStation.objects.create(
                    name=row["Truckstop Name"],
                    price_per_gallon=float(row["Retail Price"]),
                    # TEMP placeholders (see note below)
                    latitude=0.0,
                    longitude=0.0,
                )
