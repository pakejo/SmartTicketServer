from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from smarticket_api.database_handler import DatabaseHandler
from smarticket_api.models import *
from smarticket_api.serializers import *

class EventsViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = EventSerializer
    queryset = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__db_handler = DatabaseHandler()

    def list(self, request, *args, **kwargs):      
        params = request.query_params
        print(params)
        if(request.query_params and len(params) == 1):
            for key, value in params.items():
                events = self.__db_handler.get_events_by_parameter(key , value)
        else:
            events = self.__db_handler.get_all_events()
            
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        print(pk)
        event = self.__db_handler.get_event_by_id(pk)

        if event:
            serializer = EventSerializer(event, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            new_event = self.__db_handler.create_new_event(request.data)
            return Response(str(new_event.inserted_id), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            updated_event = self.__db_handler.update_event(serializer.data)

            if updated_event is None:
                return Response({'msg': 'The event does not exist'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        self.__db_handler.delete_event(pk)
        return Response(status=status.HTTP_200_OK)

class SalesViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = SaleSerializer
    queryset = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__db_handler = DatabaseHandler()

    def list(self, request, *args, **kwargs):      
        params = request.query_params
        print(params)
        if(request.query_params and len(params) == 1):
            for key, value in params.items():
                sales = self.__db_handler.get_sales_by_parameter(key , value)
        else:
            sales = self.__db_handler.get_all_sales()
            
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        event = self.__db_handler.get_sale_by_id(pk)

        if event:
            serializer = SaleSerializer(event, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = SaleSerializer(data=request.data)

        if serializer.is_valid():
            """
            TODO: Insertar lógica para el smart contract
            """
            new_sale = self.__db_handler.create_new_sale(request.data)
            return Response(str(new_sale.inserted_id), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        self.__db_handler.delete_sale(pk)
        return Response(status=status.HTTP_200_OK)
