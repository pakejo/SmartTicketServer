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

    def create(self, validated_data):
        coordinates_data = validated_data.pop('coordinates')
        new_coordinates, _ = Coordinates.objects.get_or_create(lat=coordinates_data['lat'], lng=coordinates_data['lng'])
        location, _ = Location.objects.get_or_create(coordinates=new_coordinates, **validated_data)
        return location

    def update(self, instance, validated_data):
        data = LocationSerializer(validated_data).data
        # Update location (nested serializer)
        coordinates_serializer = self.fields['coordinates']
        coordinates_instance = instance.coordinates
        coordinates_data = data.pop('coordinates')
        coordinates_serializer.update(coordinates_instance, coordinates_data)
        # Update location
        return super(LocationSerializer, self).update(instance, data)


class EventSerializer(serializers.ModelSerializer):
    imageUrl = serializers.ImageField(required=False)
    location = LocationSerializer()

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location_serializer = LocationSerializer(data=location_data)
        _ = location_serializer.is_valid()
        location = location_serializer.create(location_serializer.validated_data)
        event, _ = Event.objects.get_or_create(location=location, **validated_data)
        return event

    def update(self, instance, validated_data):
        # Update location (nested serializer)
        location_serializer = self.fields['location']
        location_instance = instance.location
        location_data = validated_data.pop('location')
        location_serializer.update(location_instance, location_data)
        # Update event
        return super(EventSerializer, self).update(instance, validated_data)


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
