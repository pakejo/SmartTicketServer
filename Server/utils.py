from pymongo import MongoClient
from helpers import get_sample_events, get_sample_sales

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

collectionEvents = db["events"]
#get_sample_events(collectionEvents)

get_sample_sales(db["sales"], db["events"])


