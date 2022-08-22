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

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid()
        event = serializer.save()

        smart_contract = SmartTicketContract(event.promoter, None, event.price)
        address, abi = smart_contract.deploy_new_contract()

        event_contract = Contract.objects.create(
            event=event,
            address=address,
            abi=abi
        )
        event_contract.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        current_event = Event.objects.get(pk=event_id)
        promoter = current_event.promoter
        customer = User.objects.get(pk=customer_id)
        contract = Contract.objects.get(event=current_event)

        smart_contract = SmartTicketContract(promoter, customer, price)
        smart_contract.set_contract(contract.address, contract.abi)
        payment_hash, token_id = smart_contract.confirm_purchase()
        refund_hash = smart_contract.refund_seller()

        sale = Sale.objects.create(
            event=current_event,
            customerId=customer_id,
            date=datetime.now(),
            purchaseHash=payment_hash,
            refundHash=refund_hash,
            token=token_id
        )
        sale.save()
        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, url_path="user/(?P<uid>\w+)")
    def user_sales(self, request, uid):
        queryset = self.queryset.filter(customerId=uid)
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ContractViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    @action(detail=False, methods=['post'])
    def owner_of(self, request):
        contract = Contract.objects.get(address=request.data['contract'])
        smart_contract = SmartTicketContract(None, None, 0)
        smart_contract.set_contract(contract.address, contract.abi)
        owner_address = smart_contract.get_owner_of(request.data['token'])
        return Response(owner_address, status=status.HTTP_200_OK)
