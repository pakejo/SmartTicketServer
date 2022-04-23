from rest_framework import viewsets, status
from rest_framework.response import Response
from bson import ObjectId

from .database_handler import DatabaseHandler
from .serializers import *
from .models import *


class EventsViewsets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__db_handler = DatabaseHandler()

    def list(self, request, *args, **kwargs):
        events = self.__db_handler.get_all_events()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
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
