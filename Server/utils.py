from pymongo import MongoClient


def get_db_handle():
    client = MongoClient(host="mongodb+srv://smarticket.zau1q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                         port=int(27017),
                         username="client-user",
                         password="paquejoivan",
                         tls=True
                         )
    db_handle = client["smarticket"]
    return db_handle
