from django.db import models


# lets us explicitly set upload path and filename
def upload_to(_instance, filename):
    return 'images/{filename}'.format(filename=filename)


class User(models.Model):
    USER_ROLES = [
        ('USER', 'user'),
        ('STAFF', 'staff'),
        ('PROMOTER', 'promoter'),
        ('ADMIN', 'admin')
    ]
    uid = models.CharField(max_length=40, default='', primary_key=True, auto_created=False)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    user_role = models.CharField(max_length=10, choices=USER_ROLES, default='USER')
    wallet_hash = models.CharField(max_length=50, blank=True)


class Category(models.Model):
    name = models.CharField(primary_key=True, auto_created=False, max_length=20, blank=False)


class Coordinates(models.Model):
    lat = models.DecimalField(max_digits=12, decimal_places=8)
    lng = models.DecimalField(max_digits=12, decimal_places=8)


class Location(models.Model):
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postalCode = models.IntegerField()
    coordinates = models.ForeignKey(Coordinates, related_name='coordinates', on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    promoter = models.ForeignKey(User, related_name='promoter', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE)
    imageUrl = models.ImageField(upload_to=upload_to, blank=True, null=True)


class Sale(models.Model):
    event = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    customerId = models.CharField(max_length=32, null=False)
    price = models.DecimalField(max_digits=7, decimal_places=5)
