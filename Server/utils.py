from pymongo import MongoClient


def get_db_handle():
    client = MongoClient(host="mongodb+srv://smarticket.zau1q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                         port=int(27017),
                         username="client-user",
                         password="paquejoivan"
                         )
    db_handle = client["smarticket"]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]


db, client = get_db_handle()
collection_handle = get_collection_handle(db, "events")

for document in collection_handle.find():
    print(document)
