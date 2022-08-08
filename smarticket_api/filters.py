from django_filters import rest_framework as filters

from smarticket_api.models import Event


class EventsFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'id': ['gte'],
            'name': ['exact', 'icontains'],
            'category__name': ['exact', 'icontains'],
            'date': ['exact', 'gte', 'lte']
        }
        exclude = ['imageUrl']
