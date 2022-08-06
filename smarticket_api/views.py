import datetime

from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from smarticket_api.serializers import *


class EventsViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Event.objects.all()

    def get_queryset(self):
        if len(self.request.query_params) >= 1:
            q_objects = Q()
            for param, value in self.request.query_params.items():
                q_objects &= Q(**{param: value})
            return self.queryset.filter(q_objects)
        else:
            return self.queryset

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
