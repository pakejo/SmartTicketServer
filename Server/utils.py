from pymongo import MongoClient


def get_db_handle():
    client = MongoClient(host="mongodb+srv://smarticket.zau1q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                         port=int(27017),
                         username="client-user",
                         password="paquejoivan"
                         )
    db_handle = client["SmarTicket"]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    print(db_handle[collection_name])
    return db_handle[collection_name]


db, client = get_db_handle()
get_collection_handle(db, "sample_airbnb")
