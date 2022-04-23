from bson import ObjectId
from pymongo import ReturnDocument

from Server.utils import get_db_handle


class DatabaseHandler:

    def __init__(self):
        self.__db_handler = get_db_handle()
        self.__collection = get_db_handle()["events"]

    def get_all_events(self):
        """Get a list of all events"""
        return list(self.__collection.find())

    def get_event_by_id(self, event_id):
        """
        Get a document by its ID
        :param event_id: Event ID
        :return: The document or None if the document is not found
        """
        return self.__collection.find_one({"_id": ObjectId(event_id)})

    def create_new_event(self, event):
        """
        Create a new event
        :param event: New event
        :return: New event
        """
        return self.__collection.insert_one(event)

    def update_event(self, event):
        """
        Updates and event
        :param event: New event data
        :return: The updated event
        """
        event_id = event.pop('_id')
        return self.__collection.find_one_and_replace({"_id": ObjectId(event_id)}, event,
                                                      return_document=ReturnDocument.AFTER)

    def delete_event(self, event_id):
        """
        Delete an event
        :param event_id: Event ID
        """
        return self.__collection.delete_one({"_id": ObjectId(event_id)})