from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('smarticket_api/', include('smarticket_api.urls')),
]
