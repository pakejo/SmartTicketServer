# from tokenize import String
# from bson import ObjectId
# from pymongo import MongoClient, ReturnDocument
#
#
# class DatabaseHandler:
#
#     def __init__(self):
#         self.__db_handler = self._initialise_database()
#         self.__eventsCollection = self.__db_handler["events"]
#         self.__salesCollection = self.__db_handler["sales"]
#         self.__categoriesCollection = self.__db_handler["categories"]
#
#     def _initialise_database(self):
#         client = MongoClient(host="mongodb+srv://smarticket.zau1q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
#                          port=int(27017),
#                          username="client-user",
#                          password="paquejoivan",
#                          tls=True
#                          )
#         db_handle = client["smarticket"]
#         return db_handle
#
# #i Events section
#
#     def get_all_events(self):
#         """Get a list of all events"""
#         return list(self.__eventsCollection.find())
#
#     def get_event_by_id(self, event_id):
#         """
#         Get a document by its ID
#         :param event_id: Event ID
#         :return: The document or None if the document is not found
#         """
#         return self.__eventsCollection.find_one({"_id": ObjectId(event_id)})
#
#     def get_events_by_parameter(self, key, value):
#         """
#         Get the events of a given category
#         :param category: category
#         :return: Document with events of 'category' or None if not found
#         """
#         return self.__eventsCollection.find({key: value})
#
#     def create_new_event(self, event):
#         """
#         Create a new event
#         :param event: New event
#         :return: New event
#         """
#         return self.__eventsCollection.insert_one(event)
#
#     def update_event(self, event):
#         """
#         Updates and event
#         :param event: New event data
#         :return: The updated event
#         """
#         event_id = event.pop('_id')
#         return self.__eventsCollection.find_one_and_replace({"_id": ObjectId(event_id)}, event,
#                                                       return_document=ReturnDocument.AFTER)
#
#     def delete_event(self, event_id):
#         """
#         Delete an event
#         :param event_id: Event ID
#         """
#         return self.__eventsCollection.delete_one({"_id": ObjectId(event_id)})
#
# #i Sales section
#
#     def get_all_sales(self):
#         """Get a list of all sales"""
#         return list(self.__salesCollection.find())
#
#     def get_sale_by_id(self, sale_id):
#         """
#         Get a document by its ID
#         :param sale_id: sale ID
#         :return: The document or None if the document is not found
#         """
#         return self.__salesCollection.find_one({"_id": ObjectId(sale_id)})
#
#     def create_new_sale(self, sale):
#         """
#         Create a new sale
#         :param sale: New sale
#         :return: New sale
#         """
#         return self.__salesCollection.insert_one(sale)
#
#     def delete_sale(self, sale_id):
#         """
#         Delete a sale
#         :param sale_id: Sale ID
#         """
#         return self.__categoriesCollection.delete_one({"_id": String(sale_id)})
#
#     def delete_event(self, sale_id):
#         """
#         Delete an sale
#         :param sale_id: sale ID
#         """
#         return self.__salesCollection.delete_one({"_id": ObjectId(sale_id)})
#
# #i Categories section
#
#     def get_all_categories(self):
#         """Get a list of all categories"""
#         return list(self.__categoriesCollection.find())
#
#     def get_category_by_id(self, category_id):
#         """
#         Get a document by its ID
#         :param category_id: category ID
#         :return: The document or None if the document is not found
#         """
#         return self.__categoriesCollection.find_one({"_id": ObjectId(category_id)})
#
#     def create_new_category(self, category):
#         """
#         Create a new category
#         :param category: New category
#         :return: New category
#         """
#         return self.__categoriesCollection.insert_one(category)