from django.urls import path
from rest_framework.schemas import get_schema_view

from . import views

app_name = "events_app"

urlpatterns = [
    path('events/', views.ListAllEvents.as_view(), name='events'),
]