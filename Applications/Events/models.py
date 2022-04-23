from django.db import models


# Create your models here.
class Coordinates(models.Model):
    lat = models.DecimalField(max_digits=12, decimal_places=8)
    lng = models.DecimalField(max_digits=12, decimal_places=8)


class Location(models.Model):
    address1 = models.CharField(max_length=20)
    address2 = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postalCode = models.IntegerField()
    coordinates = models.ForeignKey(Coordinates, related_name='coordinates', on_delete=models.CASCADE)


class Event(models.Model):
    _id = models.CharField(primary_key=True, auto_created=True, max_length=50, blank=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    promoter = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE)


