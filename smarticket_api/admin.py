from django.contrib import admin

# Register your models here.
from smarticket_api.models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Coordinates)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Sale)
admin.site.register(Contract)
