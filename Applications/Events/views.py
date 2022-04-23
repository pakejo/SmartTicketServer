from django.shortcuts import render
from rest_framework.generics import ListAPIView
#
from .serializers import EventSerializer
from Server.utils import retrieve_events


# Create your views here.
class ListAllEvents(ListAPIView):
    """Gets a list of all stored events"""
    serializer_class = EventSerializer

    def get_queryset(self):
        return retrieve_events()
