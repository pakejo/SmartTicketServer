import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from smarticket_api.filters import EventsFilter
from smarticket_api.serializers import *


class EventsViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = EventsFilter
    search_fields = ['=promoter__uid']
    ordering_fields = ['name']
    ordering = ['name']
    queryset = Event.objects.all()

    @action(detail=False)
    def future_events(self, request):
        future_events = self.queryset.filter(date__gt=datetime.datetime.now())
        serializer = EventSerializer(future_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def list(self, request, *args, **kwargs):
        if len(request.query_params) >= 1:
            queryset = self.queryset.filter(**request.query_params.dict())
        else:
            queryset = self.queryset

        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()

    @action(detail=True)
    def is_promoter(self, request, pk=None):
        user = self.queryset.get(uid=pk)
        return Response(user.user_role == 'PROMOTER', status=status.HTTP_200_OK)


class CategoryViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
