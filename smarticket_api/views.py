from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from smart_contract.SmartTicketContract import SmartTicketContract
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
        future_events = self.queryset.filter(date__gt=datetime.now())
        serializer = EventSerializer(future_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customerID')
        event_id = request.data.get('event')
        price = float(request.data.get('price'))

        event = Event.objects.get(pk=event_id)
        promoter = event.promoter
        customer = User.objects.get(pk=customer_id)

        contract = SmartTicketContract(promoter, customer, event_id, price)
        purchase_hash = contract.confirm_purchase()
        received_hash = contract.confirm_received()
        refund_hash = contract.refund_seller()

        sale = Sale.objects.create(
            event=event,
            customerId=customer_id,
            date=datetime.now(),
            price=price,
            contractAddress=contract.get_contract_address(),
            purchaseHash=purchase_hash,
            receivedHash=received_hash,
            refundHash=refund_hash
        )
        sale.save()
        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = User.objects.all()

    @action(detail=True)
    def is_promoter(self, request, pk=None):
        user = self.queryset.get(uid=pk)
        return Response(user.user_role == 'PROMOTER', status=status.HTTP_200_OK)


class CategoryViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
