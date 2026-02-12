from django.db import models

# Create your models here.
class FuelStation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price_per_gallon = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.price_per_gallon}"