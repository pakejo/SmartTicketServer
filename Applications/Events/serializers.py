from rest_framework import serializers

#
from .models import *


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer()

    class Meta:
        model = Location
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    _id = serializers.CharField(required=False)

    class Meta:
        model = Event
        fields = '__all__'

