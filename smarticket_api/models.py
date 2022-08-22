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
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    user_role = models.CharField(max_length=10, choices=USER_ROLES, default='USER')
    wallet_hash = models.CharField(max_length=50, blank=True)
    wallet_private_key = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(primary_key=True, auto_created=False, max_length=20, blank=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Coordinates(models.Model):
    lat = models.DecimalField(max_digits=12, decimal_places=8)
    lng = models.DecimalField(max_digits=12, decimal_places=8)

    class Meta:
        verbose_name_plural = 'Coordinates'


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
    price = models.DecimalField(max_digits=6, decimal_places=5)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE)
    imageUrl = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    event = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    customerId = models.CharField(max_length=32, null=False)
    date = models.DateTimeField(null=True)
    purchaseHash = models.CharField(max_length=70, blank=True, null=True)
    refundHash = models.CharField(max_length=70, blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.event.name} - {self.customerId}"


class Contract(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    address = models.CharField(max_length=70, blank=True, null=True)
    abi = models.JSONField()

    def __str__(self):
        return f"{self.event} - {self.address}"
